from pydub import AudioSegment
from pydub.utils import make_chunks
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()
file_ex = filepath.split(".")
file_ex = str(file_ex[1])
print(file_ex)
myaudio = AudioSegment.from_file(filepath, file_ex) 
chunk_length_ms = 1000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")
