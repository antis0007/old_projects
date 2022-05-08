import tkinter as tk
from tkinter import *
from tkinter import filedialog
window = tk.Tk()
window.title('Video Options (Frame testing menu)')
window.geometry('300x300') #MAKE THIS DYNAMICALLY SCALE
 
l = tk.Label(window, bg='white', width=20, text='empty')
l.pack()
framesize_text = "null"
framesize_display = tk.Label(window, bg='white', width=20, text=framesize_text)
#framesize_display.pack()
generation_count = 0
def generate_rkf():
    generation_count = generation_count + 1
    generation_counter.config(text=generation_count)
 


gen_b = Button(master, text="Gen RKF", command=generate_rkf)
gen_b.pack(anchor = W)

def browse_file():
    global data
    global framesize_text
    file = filedialog.askopenfile(parent=window,mode='rb',title='Open frame')
    if file != None:
        data = file.read()
        file.close()
        print("Debug: I got %d bytes from this file." % len(data))
        print("generation_count set to 0")

    datacomp = (str(len(data))+ " bytes, compression saves " + str(len(comp_data))) #COMP DATA IS THE FILE SIZE IN BYTES OF THE COMPRESSED FRAME
    framesize_display.config(text = datacomp)
    
    
    
    



l.config(text='Nothing Enabled') #example prints nothing enabled when start, change this to read what options are saved when opening this window when implementing
def toggle_framesize_display():
    if (var3.get() == 1):
        #framesize_display = tk.Label(window, bg='white', width=20, text='empty')
        framesize_display.pack()
    if (var3.get() == 0):
        framesize_display.pack_forget()

##def framesize_refresher():
##    global framesize_text
##    framesize_text.configure(text=data)
##    window.after(1000, refresher)

#Use var.get() == ? in if statements to access values of checkmark vars !!!!!!
        
    
def print_selection():
    if (var1.get() == 1) & (var2.get() == 0):
        l.config(text='RKF test')
    elif (var1.get() == 0) & (var2.get() == 1):
        l.config(text='Grid test')
    elif (var1.get() == 0) & (var2.get() == 0):
        l.config(text='Nothing Enabled')
    else:
        l.config(text='RKF + Grid test')
 
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Enable RKF (Lossless Compression)',variable=var1, onvalue=1, offvalue=0, command=print_selection)
c1.pack(anchor = W)
c2 = tk.Checkbutton(window, text='Enable grid interpolation (Experimental)',variable=var2, onvalue=1, offvalue=0, command=print_selection)
c2.pack(anchor = W)
c3 = tk.Checkbutton(window, text='Enable frame size display',variable=var3, onvalue=1, offvalue=0, command=toggle_framesize_display)
c3.pack(anchor = W)
#MENU CONFIG ----!
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=browse_file)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)
window.mainloop()
