import tkinter
import os
from tkinter import filedialog
from tkinter import *

import turtle
menu  = False
sizemenu  = False
res = 400
col = "black"
button_list = []
templines = []
drawsize = 1
#This version does not support alpha/transparency. Picture output will be done with .eps format, because we can only use built in libraries

def new():
    draw.clear()
    draw.penup()
    return
def save():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".eps")
    global canvas
    f.write(canvas.postscript())
    return
def load(): #This function has to parse eps files and recreate the art with turtle
    global templines
    filename = filedialog.askopenfilename(title = "Select .eps drawing file",filetypes = (("eps file","*.eps"),("all files","*.*")))
    lines = list(open(filename))
    
    eventpos = 0
    #eventpos is the line where events related to drawing begin to happen:
    #draw.pendown()
    draw.penup()
    last_stroke = 0
    curr_stroke = 0
    global templines
    for i in range(0, len(lines)):
        if lines[i].strip() == "%%EndSetup":
            eventpos = i
            print(eventpos)
            break
    last_stroke = eventpos
    for i in range(eventpos, len(lines)):
        if lines[i].strip() == "stroke":
            curr_stroke = i
            templines = []
            for x in range(last_stroke, curr_stroke):
                #print(templines)
                templines.append(lines[x])
            #print(templines)
                
                
            templines.reverse()
            #print(templines)
            
            for z in range(0, len(templines)):
                try:
                    parts = templines[z].strip().split(" ")
                    print(parts)
                    final = parts[-1]
                    
                    if final == "AdjustColor":
                        col = (float(parts[0]),float(parts[1]),float(parts[2]))
                        draw.pencolor(col)
                        print(col)
                        
                    elif final == "setlinewidth":
                        drawsize=int(parts[0])
                        draw.pensize(drawsize)
                    elif final == "moveto":
                        draw.penup()
                    elif final == "lineto":
                        draw.pendown()
                    x = int(parts[0])
                    y = int(parts[1]) - res/2
                    draw.goto(x,y) 
                
                
                
                except Exception as e:
                    print("Non-Formatted data")
                    print(e)
                
            last_stroke = curr_stroke

            
        
    return
def colour():
    
    colourlist = ["black", "white", "red", "orange", "yellow", "green", "blue", "indigo", "violet","maroon","magenta"]
    global colourlist_tkvar
    global button_list
    colourlist_tkvar = tkinter.StringVar()#create a tkinter stringvar for modifications
    
    def colchange(i):
        global col
        print(i)
        col = i
    global menu
    
    if menu == False:
        
        colourlist_tkvar.set(colourlist[0])
        for i in colourlist:
            button = Button(root, text=i, command=lambda x=i: colchange(x), bg = i)
            button.pack(side = "left")
            button_list.append(button)
        menu = True
        print(col)
        return
    if menu == True:
        for i in button_list:
            i.destroy()
        menu = False
        print(col)
        return
def size():   
    global sizemenu
    global size_scale
    def drawsize(i):
        global drawsize
        drawsize = i
    
    if sizemenu == False:
        size_scale = Scale(root, from_=0, to=20, orient=HORIZONTAL, command = drawsize)
        size_scale.pack(side = "left")
        
        sizemenu = True
        return
    if sizemenu == True:
        size_scale.pack_forget()
        sizemenu = False
        return
    

#Setup Gui

root = Tk()
root.title("Turtle Paint by Andrew Tischenko 2021")


frame = Frame(root)
frame.pack()
mainmenu = Menu(frame)
mainmenu.add_command(label = "New", command= new)
mainmenu.add_command(label = "Save", command= save)
mainmenu.add_command(label = "Load", command= load)
mainmenu.add_command(label = "Colour Menu", command= colour)
mainmenu.add_command(label = "Size Menu", command= size)
mainmenu.add_command(label = "Exit", command= root.destroy)
 
root.config(menu = mainmenu)

#def pressed(event):
    #draw.pendown()
    #print("press")
def released(event):
    draw.penup()
    
    print("release")
    
def motion(event):
    
    canvas.unbind("<B1-Motion>") #Fix recursion depth issue
    draw.color(col)
    draw.pensize(drawsize)
    draw.goto(event.x - res/2, res/2 - event.y)
    draw.pendown()
    
    
    canvas.bind("<B1-Motion>",motion)
    
canvas = tkinter.Canvas(master = root, width = res, height = res)
canvas.bind("<B1-Motion>", motion)


canvas.bind("<ButtonRelease-1>", released)
#canvas.bind("<ButtonPress-1>", pressed)
canvas.pack()

draw = turtle.RawTurtle(canvas)
draw.penup()

draw.pensize(1)
draw.speed(0)
draw.setheading(0)
draw.left(130)
#canvas.colormode(255)

canvas.mainloop()




