import csv
import os
#Create a file dialog window
import tkinter as tk
from tkinter import filedialog
import statistics

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()
def loadcsv(csvfilename):
    rowindex = 0
    data = []
    with open(csvfilename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row:
                rowindex += 1
                columns = [str(rowindex), row[0], row[1], row[2], row[3], row[4]]
                data.append(columns)
    return data

data = loadcsv(filepath)

input("Press enter to continue, this will modify your CSV data")

print("Loading CSV...")
loadcsv(filepath)
print("Done")

#Modification calculations begin here...
print("Standardizing time...")
start_time = data[1]
#print(start_time)
end_time = data[-1]
#print(end_time)
duration = (float(end_time[1])-float(start_time[1]))
print("Duration: ", duration)

print("Changing to relative time...")
starttimevar = float(data[1][1])
for i in range(1,int(end_time[0])):
    
    data[i][1] = (float(data[i][1]) - starttimevar)
    #print(data[i][1])
print("Calculating Time Differences...")
difflist = []
prev = 0
curr = 0
for i in range(1,int(end_time[0])):
    curr = data[i][1]
    difflist.append(curr-prev)
    prev = data[i][1]
averagetime = statistics.mean(difflist)
averagefreq = 1/averagetime
print("Average time interval: " , averagetime)
print("Average recording frequency: ",averagefreq)
#Append time and freq data to first line of 2d list
data[0].append(averagetime)
data[0].append(averagefreq)
op = input("--- FINAL CHECK, TYPE y TO UPDATE CSV ---")
if op == "y" :
    os.remove(filepath)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    input("Complete...")
else:
    print("Canceled...")







