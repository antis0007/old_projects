#LAB (Lossless Adaptive Binary) Compression
#Designed by Antis0007
#Project begun: 2020-05-22

#Theory:
#Scan through an entire file (in parts so it doesnt overflow your hardware RAM), Check what patterns are most prevalent
#Get hex value list, compare every 2 adjacent hex values, and store to a list how often they appear
#Replace 255 most common binary adjacent(Binary meaning 2) hex values with a new single hex value

#(basically just detecting ngram patterns)

#Keep an array of 0 and 1s representing which values have been modified
#once operations are completed, and the decode values file needs to be generated, simplify this array with every pair of 1s
#appearing as a single 1

#Save this array to a signature type file, with instructions on the correlations between the sets of common hex value pairs
# and on how to decode the file

#Result: An up to 50% compression ratio per compression, entirely lossless.

#Pros:
#stackable as many times as you need, with a high theoretical compression ratio
#more effective with larger single files

#Cons:
#Data will take quite a while to process (Probably),
#decompression requires the signature files that go along with it
#you can only (de)/compress a file smaller than your available RAM (FOR NOW)

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() #close full GUI
filepath = askopenfilename()

# BELOW GENERATES THE LIST, thus far it loads the whole thing into memory
with open(filepath, 'r') as fp:
    hex_list = ["{:02x}".format(ord(c)) for c in fp.read()]

print(hex_list)
