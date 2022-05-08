import matplotlib.pyplot as plt  
import numpy as np  
import csv
import os
#Create a file dialog window
import tkinter as tk
from tkinter import filedialog
import statistics

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()

rowindex = 0
timeindex = []
TP9=[]
AF7=[]
AF8=[]
TP10=[]
freq = ""
time = ""
with open(filepath, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    firsttime = True
    for lines in reader:
        if firsttime == True:
            firsttime= False
            freq=float(lines[7])
            time=float(lines[7])
        else:
            TP9.append(float(lines[2]))
            AF7.append(float(lines[3]))
            AF8.append(float(lines[4]))
            TP10.append(float(lines[5]))
            timeindex.append(float(lines[1]))
            


#"rotate" the 2d list to give us a single list for frequency values:
#data = loadcsv(filepath)
#rot_data= rotated = list(zip(*reversed(data)))
#print(TP9)
TP9=np.array(TP9)
AF7=np.array(AF7)
AF8=np.array(AF8)
TP10=np.array(TP10)
#print(TP9)
print(freq)
print(time)
np_timeindex =np.array([timeindex])
#print(np_timeindex)

    
dt = 0.005
t = np.arange(0.0, 20.0, dt)  
x = np.sin(np.pi * t) + 1.5 * np.cos(np.pi * 2*t)  
  
plt.specgram(TP10, Fs = freq) 
plt.title('Spectrogram of EEG signal\n',  
          fontsize = 14, fontweight ='bold')
plt.show()
