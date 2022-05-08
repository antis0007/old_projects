"""
Record from a Stream

This example shows how to record data from an existing Muse LSL stream
"""
#NOTE: This uses code from the Muse-lsl recordStream.py + startMuseStream.py example file
from muselsl import record
from muselsl import stream, list_muses
# Note: an existing Muse LSL stream is required
t= 20
if __name__ == "__main__":
    print("Welcome to the EEG/AI Data Recorder+Preprocesser! If you would like to start a connection with a muse, type c")
    comm = str(input())
    if comm == "c":
        print("placeholder")
        #Open streaming code
        
    try:    
        record(t)
    except(e):
        print("Muse LSL stream failed:")
        print(e)

    # Note: Recording is synchronous, so code here will not execute until the stream has been closed
    timestr = str('Recording period of ',  t ,'seconds has ended')
    comm = str(input(timestr))

