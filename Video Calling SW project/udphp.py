#!/usr/bin/env python3

UDP_PORT = 5555         # Default port for UDP communication
# Please, adjust MAXBUF_SIZE for optimal and WORKING values.
# 40000 looks optimal for my test environment. But, IT MAY NOT WORK IN YOUR CASE!
MAXBUF_SIZE = 40000     # Max size for TCP data. Must be < 2^16 (to fit struct.pack format: 'H')
HEADER_SIZE =    16     # 1:msgtype + 2:seqno + 2:buflen + 11:checksum
#   TOTAL   = 40016     # Max size for UDP data (MAXBUF_SIZE+HEADER_SIZE)
# I repeat: Large UDP packets e.g. > 40KB (or even 30KB) may not be transmitted at all!
# Also, small values like 1.4KB will be very inefficient for graphical apps like VNC!
DIGEST_SIZE = HEADER_SIZE-5   # Only that many bytes from MD5SUM will be used for digest
# Format of UDP data transmitted:
#  [0:1] = Message type indicating:
#   'A' : Positive ack
#   'N' : Negative ack
#   'H' : Heartbeat (keep alive) message
#   'U' : Data message which contains uncompressed buffer
#   'C' : Data message which contains compressed buffer
#  [1:3] = Sequence number to keep track UDP packets
#  [3:5] = Length of (uncompressed original) buffer data
# [5:16] = Digest or checksum of the (uncompressed, original) buffer data
#  [16:] = Buffer containing (TCP) data (possibly compressed)

# === Parse command line arguments:
import argparse
parser = argparse.ArgumentParser(description='''UDP Hole Puncher. Ver. 0.12
\N{COPYRIGHT SIGN} 2019-02-08 Fedon Kadifeli''',
  formatter_class=argparse.RawDescriptionHelpFormatter,
  epilog='''modes of operation:
  server mode: udphp.py -c [-d] tcp_conn_port   client_public_ip [udp_port]
  client mode: udphp.py -l [-d] tcp_listen_port server_public_ip [udp_port]''')
parser.add_argument("-d", "--debug",  help="print extra debug info to stderr", action="store_true")
pmode = parser.add_mutually_exclusive_group(required=True)
pmode.add_argument("-c", "--connect", help="'server' side mode; connect to local TCP port", action="store_true")
pmode.add_argument("-l", "--listen",  help="'client' side mode; listen to local TCP port",  action="store_true")
parser.add_argument("tcp_port", help="TCP port for connection (when running on the server) or TCP port for listening (when running on the client)", type=int)
parser.add_argument("udp_pub_ip", help="peer's public IP")
parser.add_argument("udp_port", help="UDP port for communication with peer (default "+str(UDP_PORT)+")", type=int, nargs='?', default=UDP_PORT)
ARGS = parser.parse_args()
del parser, pmode

# Set up error logging:
import logging
logging.basicConfig(level=logging.DEBUG if ARGS.debug else logging.WARNING,
  format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%H:%M:%S')
##logging.debug('Debug!'); logging.info('Info!'); logging.warning('Warn!'); logging.error('Error!')

import socket, time, sys, os, threading, struct, random

MAX_SEQNO_BITS = 0xFFFF     # Must be a number like (2^n-1) < 2^16 (to fit struct.pack format: 'H')
ACKED_SEQNO = -1            # Sequence number of received ack
ACKED_OK = False            # Received ack type
HB_SMSG = b'HELOCLNT'       # Heartbeat messages
HB_RMSG = b'HELOSRVR'
HB_COUNT = 0                # To keep track of heartbeat timeout
TOT_ORIGDATA = 0            # Length of data send (original)
TOT_COMPDATA = 0            # Length of real data send (possibly compressed)
SERVER_MODE = True
if ARGS.listen:             # Client side mode
  SERVER_MODE = False
  HB_SMSG, HB_RMSG = HB_RMSG, HB_SMSG

MY_IP = ''
PEER_IP = socket.gethostbyname(ARGS.udp_pub_ip)
UDP_PORT = ARGS.udp_port
TCP_PORT = ARGS.tcp_port
del ARGS

logging.warning('Server_Mode={} Local_TCP_Port={} Peer_Public_IP={} Peer_UDP_Port={}'.format(SERVER_MODE, TCP_PORT, PEER_IP, UDP_PORT))

# Prepare UDP for hearbeat thread:
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((MY_IP, UDP_PORT))

# === Class: Heartbeat_Thread ===
class Heartbeat_Thread(threading.Thread):
  def __init__(self, name=None, args=(), kwargs=None):
    super().__init__()
    self.name = name
  def run(self):
    global HB_COUNT
    logging.warning(self.name+'Started.')
    stat_count=0
    while HB_COUNT<10:
      HB_COUNT+=1       # HB_COUNT is reset to 0 when a heartbeat message is received by UDPReceive_Thread
      udp_sock.sendto(HB_SMSG, (PEER_IP, UDP_PORT))
      logging.debug(self.name+'Sent: '+str(HB_SMSG))
      time.sleep(10 * (2+random.random()) )
      stat_count+=1
      if (TOT_ORIGDATA>0) and (stat_count>15):
        stat_count=0
        logging.warning(self.name+'Cumul. compr. ratio: {:.4}'.format(TOT_COMPDATA/TOT_ORIGDATA))
    logging.error(self.name+'No heartbeat signal for a while: Exiting...')
    os._exit(14)
# End of Heartbeat_Thread

Heartbeat_Thread(name='HTBT: ').start()

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if SERVER_MODE:
  tcp_sock.connect(('', TCP_PORT))
  logging.warning('Connected to local TCP port {}'.format(TCP_PORT))
  tcp_conn = tcp_sock
else:
  tcp_sock.bind(('', TCP_PORT))
  logging.warning('Listening for connection on local TCP port {}'.format(TCP_PORT))
  tcp_sock.listen(1)
  tcp_conn, addr = tcp_sock.accept()

ack_event = threading.Event()   # For synchronization of ack receipts

# === Helper functions ===
def calculate_digest(b):
  from hashlib import md5
  return md5(b).digest()[:DIGEST_SIZE]
# calculate_digest

def attempt_compr(buf, buflen):
  from zlib import compress
  MIN_GAIN=100
  global TOT_COMPDATA, TOT_ORIGDATA
  TOT_ORIGDATA += buflen
  if buflen>MIN_GAIN:
    compr_buf = compress(buf)
    compr_buflen = len(compr_buf)
    if compr_buflen<(buflen-MIN_GAIN):
      TOT_COMPDATA += compr_buflen
      return b'C', compr_buf, compr_buflen
  # No significant gain from compression
  TOT_COMPDATA += buflen
  return b'U', buf, buflen
# attempt_compr

def attempt_decompr(buf):
  from zlib import decompress
  try:
    dec_buf = decompress(buf)
    return dec_buf
  except Exception as e:
    logging.warning('Decompress: '+e)
    return b''
# attempt_decompr
# End of Helper functions

# === Class: UDPSend_Thread ===
class UDPSend_Thread(threading.Thread):
  def __init__(self, name=None, args=(), kwargs=None):
    super().__init__()
    self.name = name
  def run(self):
    global ACKED_SEQNO, ACKED_OK
    logging.warning(self.name+'Started.')
    seqno = 0
    while True:
      try:
        inbuf = tcp_conn.recv(MAXBUF_SIZE)
      except:
        logging.error(self.name+'TCP connection lost: Exiting...')
        os._exit(11)
      if not inbuf:
        logging.error(self.name+'TCP connection closed (EOF): Exiting...')
        os._exit(12)
      buflen = len(inbuf)
      digest = calculate_digest(inbuf)
      compr_status, inbuf, cbuf_len = attempt_compr(inbuf, buflen)
      data = struct.pack('!sHH{}s{}s'.format(DIGEST_SIZE, cbuf_len), compr_status, seqno, buflen, digest, inbuf)
      ACKED_OK = False
      for retry in range(30):
        udp_sock.sendto(data,(PEER_IP, UDP_PORT))
        ack_event.clear()
        ack_event.wait(1)
        if (ACKED_SEQNO==seqno) and ACKED_OK:
          break
        logging.warning(self.name+'Retry sending: seqno={}.{} len={} retry={} digest={} inbuf={}'.format(seqno, ACKED_OK, buflen, retry+1, digest.hex(), inbuf[:10]))
      else:
        logging.error(self.name+'No valid response from UDP peer: Exiting...')
        os._exit(15)
      logging.debug(self.name+'Successfully sent: seqno={} len={} retry={} digest={} inbuf={}'.format(seqno, buflen, retry, digest.hex(), inbuf[:10]))
      seqno = (seqno+1) & MAX_SEQNO_BITS
# End of UDPSend_Thread

# === Class: UDPReceive_Thread ===
class UDPReceive_Thread(threading.Thread):
  def __init__(self, name=None, args=(), kwargs=None):
    super().__init__()
    self.name = name
  def run(self):
    logging.warning(self.name+'Started.')
    expected_seqno = 0
    while True:
      data, addr = udp_sock.recvfrom(MAXBUF_SIZE+HEADER_SIZE)
      msg_type = data[:1]
      if msg_type==b'H':
        # Heartbeat message
        global HB_COUNT
        HB_COUNT = 0
        logging.debug(self.name+'Keep alive packet={}'.format(data))    # Log and ignore it
      elif msg_type in b'AN':
        # Positive or negative ack.
        global ACKED_SEQNO, ACKED_OK
        ACKED_OK = msg_type == b'A'
        ACKED_SEQNO, = struct.unpack('!H', data[1:3])
        ack_event.set()
        logging.debug(self.name+'{}tive ack. for seqno={}'.format('Posi' if ACKED_OK else 'Nega', ACKED_SEQNO))
      elif msg_type in b'CU':
        # Compressed or uncompressed data buffer
        sent_seqno, sent_buflen, sent_digest = struct.unpack('!HH{}s'.format(DIGEST_SIZE), data[1:HEADER_SIZE])
        outbuf = data[HEADER_SIZE:]
        if msg_type == b'C':
          outbuf = attempt_decompr(outbuf)
        buflen = len(outbuf)
        digest = calculate_digest(outbuf)
        if (sent_seqno==expected_seqno) and (sent_buflen==buflen) and (sent_digest==digest):
          # Everything is OK!
          try:
            tcp_conn.send(outbuf)
          except:
            logging.error(self.name+'TCP connection lost: Exiting...')
            os._exit(13)
          udp_sock.sendto(struct.pack('!sH', b'A', sent_seqno), (PEER_IP, UDP_PORT))     # Send positive ack.
          logging.debug(self.name+'Valid data: seqno={} len={} digest={} outbuf={}'.format(expected_seqno, buflen, digest.hex(), outbuf[:10]))
          expected_seqno = (expected_seqno+1) & MAX_SEQNO_BITS
        else:
          # Data error or old packet
          if expected_seqno>sent_seqno:
            # Old packet; resend positive ack.
            udp_sock.sendto(struct.pack('!sH', b'A', sent_seqno), (PEER_IP, UDP_PORT))
            packet_err = 'Old'
          else:
            # Corrupted packet; send negative ack.
            udp_sock.sendto(struct.pack('!sH', b'N', expected_seqno), (PEER_IP, UDP_PORT))
            packet_err = 'Corrupted'
          logging.warning(self.name+packet_err+' packet: sent_seqno={} ? expected_seqno={} / sent_len={} ? len={} / sent_digest={} ? digest={}'.format(
            sent_seqno, expected_seqno, sent_buflen, buflen, sent_digest.hex(), digest.hex()))
      else:
        # Message type error
        logging.warning(self.name+'Type error: msg_type={} data: sent_seqno={} ? expected_seqno={} / sent_len={} ? len={} / sent_digest={} ? digest={}'.format(
          msg_type, sent_seqno, expected_seqno, sent_buflen, buflen, sent_digest.hex(), digest.hex()))
        logging.error(self.name+'Invalid message type. Exiting...')
        os._exit(16)
# End of UDPReceive_Thread

UDPSend_Thread(name='SEND: ').start()
UDPReceive_Thread(name='RECV: ').start()
