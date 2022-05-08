#Mass Organizer for _final files
#.ass Format
import shutil
import tkinter
import os
from tkinter import filedialog
from tkinter import *

pairs = 0 #number of pairs

root = Tk()
root.title("Mass Organizer for _final files")
files = filedialog.askopenfilenames(title = "Select .ass _final sub files",filetypes = (("Subtitle File","*.ass"),("all files","*.*")))

workingdir = os.getcwd()
foldername = input(str("Folder Name: "))

if not os.path.exists(foldername):
    os.mkdir(foldername)
folderpath = os.path.join(workingdir,foldername)

filenum = 0
for file in files:
    filenum += 1
    path = os.path.abspath(file)
    print("path: ")
    print(path)
    direc = os.path.dirname(file)
    filenumstr = str(filenum)
    new = os.path.join(folderpath,str(foldername+"_"+filenumstr+".ass"))
    shutil.copyfile(path, new)

root.mainloop()

        
    
