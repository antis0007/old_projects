from scipy import signal
from scipy.fft import fftshift
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
with open(filepath, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    firsttime = True
    for lines in reader:
        if firsttime == True:
            firsttime= False
            freq=float(lines[7])
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
np_timeindex =np.array([timeindex])
#print(np_timeindex)


#Scipy part
fs = 10e3
N = 1e5
amp = 2 * np.sqrt(2)
noise_power = 0.01 * fs / 2
time = np.arange(N) / float(fs)
mod = 500*np.cos(2*np.pi*0.25*time)
carrier = amp * np.sin(2*np.pi*3e3*time + mod)
noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
noise *= np.exp(-time/5)
x = carrier + noise
print(x)
print(TP9)
#print(fs)
f, t, Sxx = signal.spectrogram(TP10, freq )
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
