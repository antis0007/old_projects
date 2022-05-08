#Simple Subtitle Parser, pair calculator for character
#.ass Format

import tkinter
import os
from tkinter import filedialog
from tkinter import *

pairs = 0 #number of pairs

root = Tk()
root.title("Simple Character Pair Calculator")
files = filedialog.askopenfilenames(title = "Select .ass sub files",filetypes = (("Subtitle File","*.ass"),("all files","*.*")))
   
char = str(input("Input character name to check for conversational pairs: "))

for file in files:
    lines = list(open(file))    
    for i in range(0, len(lines)):
        try:
            Start, End, Character, Text = lines[i].split(",",3)
            if char == Character:
                pairs = pairs+1
               
                    
        except:
            print("Non-Formatted data on line " , i)
print(pairs)

root.mainloop()

        
    
