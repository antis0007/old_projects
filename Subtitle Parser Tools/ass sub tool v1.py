#Simple Subtitle Parser, Reformatter and Annotator:
#.ass Format

import tkinter
import os
from tkinter import filedialog
from tkinter import *

root = Tk()
root.filename =  filedialog.askopenfilename(title = "Select .ass sub file",filetypes = (("Subtitle File","*.ass"),("all files","*.*")))
#print (root.filename)

filename = os.path.splitext(root.filename)[0]
ext = os.path.splitext(root.filename)[1]
print(filename)
print(ext)
#Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
#Dialogue: 0,0:00:04.48,0:00:08.90,Default,,0000,0000,0000,,The universe has a beginning, but no end.
#Preprocess:
#Split into 9 commas,
lines = list(open(root.filename))

##for line in lines:
##    Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = line.strip().split(",",9) #Call strip to deal with /n
##    print(Text)
eventpos = 0
#eventpos is the line where events in subs begin to happen:
for i in range(0, len(lines)):
    if lines[i].strip() == "[Events]":
        eventpos = i
        print(eventpos)
        break

lines_clean_name = (filename+ "_clean"+ ext)
lines_clean = open((lines_clean_name), "w") #full write to reset
lines_clean.write("")
lines_clean.close()
lines_clean = open((lines_clean_name), "a")#Now open in append mode, to add new lines to clean version
                   
Character = "" #Character is left blank in the initial cleaning of subtitle format
                   
for i in range(eventpos+7, len(lines)): #+7 to begin at where lines start
    try:
        #Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].strip().split(",",9) #Call strip to deal with /n
        Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].split(",",9) #removed strip bc this is intermediate step, keep in mind for display purposes though.
        print(Text)
        
        #NEW FORMAT: Start, End, Character, Text
        lines_clean.write((Start+","+End+","+Character+","+Text))
        
        
        
    except:
        print("Non-Formatted data on line " , i)
lines_clean.close()
#Use labels to display all lines from the subs
    
        
    
