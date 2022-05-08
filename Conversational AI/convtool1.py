#Conversational AI NLP project
#Objective: seq2seq chatbot using scripts.

#GUI
import tkinter
import os
import re
from tkinter import filedialog
from tkinter import *

from tensorflow import keras
import tensorflow as tf
import numpy as np

root = Tk()
root.title("Conversational AI NLP project")


def preprocess_sentence(w):
    w = re.sub(r"([?.!,¿])", r" \1 ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
    w = w.strip()
    #Add start and end tokens
    w = '<start> ' + w + ' <end>'
    return w
character = input("Enter character name: ")

files = filedialog.askopenfilenames(title = "Select subtitle files",filetypes = (("Subtitle File","*.ass"),("all files","*.*")))
for file in files:
    lines = list(open(file))    
    for i in range(0, len(lines)): #+x to begin at where lines start
        try:
            Start, End, Character, Text = lines[i].split(",",4)
            print(Text)
            preprocess_Text = preprocess_sentence(Text)
            print(preprocess_Text)        
            
        except:
            print("Non-Formatted data on line " , i)
lines_clean.close()


