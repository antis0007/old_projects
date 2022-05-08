import tkinter
import os
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title("Mass Sub Tool v9")
files = filedialog.askopenfilenames(title = "Select .ass sub files",filetypes = (("Subtitle File","*.ass"),("all files","*.*")))


for file in files:
    lines = list(open(file))    
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1]
    print(filename)
    print(ext)
    #Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    #Dialogue: 0,0:00:04.48,0:00:08.90,Default,,0000,0000,0000,,The universe has a beginning, but no end.
    #Preprocess:
    #Split into 9 commas,
    lines = list(open(file))

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
                       
    for i in range(eventpos, len(lines)): #+x to begin at where lines start
        try:
            #Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].strip().split(",",9) #Call strip to deal with /n
            Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].split(",",9) #removed strip bc this is intermediate step, keep in mind for display purposes though.
            
            
            #NEW FORMAT: Start, End, Character, Text
            lines_clean.write((Start+","+End+","+Style+","+Text))
            
            
            
        except:
            print("Non-Formatted data on line " , i)
    lines_clean.close()
    lines_clean = list(open((lines_clean_name), "r"))
    lines_final_name = (filename+ "_final"+ ext)
    lines_final = open((lines_final_name), "w") #full write to reset
    lines_final.write("")
    lines_final.close()
    lines_final = open((lines_final_name), "a")#Now open in append mode, to add new lines to clean version
    for i in range(0, len(lines_clean)):
        #newlinestr = str(lines_clean[i]+'\n')
        lines_final.write(lines_clean[i])
    print("Saved")
    
root.mainloop()

        
    
