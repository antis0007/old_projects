#Python audiobook splitter:
#by Andrew Tischenko - 2020-09-04
#Dependencies: python3+, ffmpeg, pydub
import tkinter as tk
from tkinter import filedialog
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()
file_ex = filepath.split(".")
file_ex = str(file_ex[1])
print(file_ex)
padding = int(input("Input silence padding in ms: "))
split_time = int(input("Input silence time before split in ms: "))
keep_var = int(input("Input silence to keep at beginning and end: (default 1000ms)"))
book = AudioSegment.from_file(filepath)
print(book.dBFS)
silence_thresh_var = int(input("Input silence threshold before split in dBFS: (take value above and subtract an amount) "))
test = pydub.utils.get_prober_name()
print(test)


def match_target_amplitude(aChunk, target_dBFS):
    #Normalize chunks
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

chunks = split_on_silence(book, min_silence_len = split_time,silence_thresh = silence_thresh_var, keep_silence = keep_var)
for i, chunk in enumerate(chunks):
    silence_chunk = AudioSegment.silent(duration=padding) #ms padding

    audio_chunk = silence_chunk + chunk + silence_chunk

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    print("Exporting chunk{0}.mp3.".format(i))
    normalized_chunk.export(
        ".//chunk{0}.mp3".format(i),
        bitrate = "192k",
        format = "mp3"
    )

