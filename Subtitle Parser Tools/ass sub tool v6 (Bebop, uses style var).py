#Simple Subtitle Parser, Reformatter and Annotator:
#.ass Format

import tkinter
import os
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title("Simple .ass Sub Tool")
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


def save():
    lines_final_name = (filename+ "_final"+ ext)
    lines_final = open((lines_final_name), "w") #full write to reset
    lines_final.write("")
    lines_final.close()
    lines_final = open((lines_final_name), "a")#Now open in append mode, to add new lines to clean version
    for i in range(0, len(lines_clean)):
        #newlinestr = str(lines_clean[i]+'\n')
        lines_final.write(lines_clean[i])
    print("Saved")
        
 
 
def loadcharacters(): #Load characters has to load the character file and wipe any previous character file + associated GUI
    root.characterfile =  filedialog.askopenfilename(title = "Select character file",filetypes = (("Text file","*.txt"),("all files","*.*")))
    character_list = list(open((root.characterfile), "r"))
    global button
    button.destroy()
    #character_list = []


    
    for i in character_list:
        button = Radiobutton(root, text=i, variable=character_list_tkvar, value=i, command=setchar)
        button.pack(side = "top")

def setchar(): #basic function to set the value of char, has to be made bc of tk commands // UPDATED to also set string values.
    global char
    char = character_list_tkvar.get().strip() #remember to strip /n
    print(char)
    selec = lines_clean_gui.curselection()[0]
    #Reformatting:
    Start, End, Character, Text = lines_clean[selec].split(",",3)
        
    #Replace Character with char
        
    #NEW FORMAT: Start, End, char, Text
    lines_clean[selec]=((Start+","+End+","+char+","+Text))
                          
    #Update GUI:
    lines_clean_tkvar.set(lines_clean)


    
frame = Frame(root)
frame.pack()
mainmenu = Menu(frame)
mainmenu.add_command(label = "Save", command= save)  
mainmenu.add_command(label = "Load Characters", command= loadcharacters)
mainmenu.add_command(label = "Exit", command= root.destroy)
 
root.config(menu = mainmenu)
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
                   
for i in range(eventpos+1, len(lines)): #+1 to begin at where lines start
    try:
        #Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].strip().split(",",9) #Call strip to deal with /n
        Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text = lines[i].split(",",9) #removed strip bc this is intermediate step, keep in mind for display purposes though.
        print(Text)
        
        #NEW FORMAT: Start, End, Character, Text
        #v6 uses STYLE instead of name or blank Character variable, This is because some subs use style as the variable for character names (Cowboy Bebop)
        lines_clean.write((Start+","+End+","+Style+","+Text))
        
        
        
    except:
        print("Non-Formatted data on line " , i)
lines_clean.close()
#Use labels to display all lines from the subs

#GUI:

root.geometry("1280x720")



def delete(event):
    selected = lines_clean_gui.curselection()
    for i in selected[::-1]:
        lines_clean.pop(i)        
    lines_clean_tkvar.set(lines_clean)
    #deselection:
    #lines_clean_gui.selection_clear(0, tkinter.END)

def select(event):
    i = lines_clean_gui.curselection()[0]
    item.set(lines_clean[i])

def update(event):
    i = lines_clean_gui.curselection()[0]
    lines_clean[i] = item.get()
    lines_clean_tkvar.set(lines_clean)

def up(event):
    selected = lines_clean_gui.curselection()[0]
    selected += -1
    lines_clean_gui.select_set(selected)
    
def down(event):
    selected = lines_clean_gui.curselection()[0]
    selected += 1
    lines_clean_gui.select_set(selected)

h = Scrollbar(root, orient = 'horizontal')
h.pack(side = BOTTOM, fill = X)


v = Scrollbar(root)
v.pack(side = RIGHT, fill = Y)

lines_clean = list(open((lines_clean_name), "r"))
lines_clean_tkvar = tkinter.StringVar(value=lines_clean)#create a tkinter stringvar for modifications
lines_clean_gui = Listbox(root, listvariable=lines_clean_tkvar, xscrollcommand = h.set, yscrollcommand = v.set, selectmode='extended')
lines_clean_gui.bind('<<ListboxSelect>>', select)

#for i in range(0, len(lines_clean)):
    #lines_clean_gui.insert(END,lines_clean[i])


lines_clean_gui.pack(side="left",fill="both", expand=True)
root.iconify() #Unclick and reclick, scuffed solution but it works!
root.deiconify()
lines_clean_gui.bind('<Delete>', delete)
lines_clean_gui.bind('<Up>', up)
lines_clean_gui.bind('<Down>', down)

h.config(command=lines_clean_gui.xview)
v.config(command=lines_clean_gui.yview)

character_list = ["None"]

character_list_tkvar = tkinter.StringVar()#create a tkinter stringvar for modifications
character_list_tkvar.set(character_list[0])

#character_list_gui = Listbox(root, listvariable=character_list_tkvar, selectmode='browse')
#character_list_gui.pack(side="right",fill="both", expand=True)
for i in character_list:
    button = Radiobutton(root, text=i, variable=character_list_tkvar, value=i, command=setchar)
    button.pack(side = "bottom")
    
item = tkinter.StringVar()
entry = tkinter.Entry(root, textvariable=item, width=20)
entry.pack(side="right",fill="both", expand=True)
entry.bind('<Return>', update)

root.mainloop() 

        
    
