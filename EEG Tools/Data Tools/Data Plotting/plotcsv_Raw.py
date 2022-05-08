import matplotlib.pyplot as plt
import csv
#Create a file dialog window
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filepath = filedialog.askopenfilename()

x=[]
y=[]
#SIMPLE UTILITY TO DISPLAY A CSV FILE
with open(filepath, 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    i=0
    for row in plots:
        if i == 0:
            plt.xlabel(row[0])
            plt.ylabel(row[1])
        
        if i > 0:
            x.append(float(row[0]))
            y.append(float(row[1]))
        i=i+1


plt.plot(x,y, marker='o')

plt.title('')

plt.xlabel('Time')
plt.ylabel('Freq')

plt.show()
