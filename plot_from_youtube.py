from __future__ import unicode_literals
import youtube_dl
import numpy as np
import wave
import time
import math
import struct
from math import sqrt
import pyaudio
import terminalsize
import time


def ydl(URL):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':'ydlaudiodata.%(ext)s',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '320',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])

print("input an URL from youtube(https://):")
s=input()
if s!="":
    ydl(s)




terminalsize=terminalsize.get_terminal_size()
print("Download Finished.")
print("Processing...please wait.")
print("This may take a few minutes")
if __name__ == '__main__':
    # Open the wave file and get info
    wave_file = wave.open('ydlaudiodata.wav', 'r')
    data_size = wave_file.getnframes()
    channel=wave_file.getnchannels()
    sample_rate = wave_file.getframerate()
    sample_width = wave_file.getsampwidth()
    #print(wave_file.getparams())
    sample_width = wave_file.getsampwidth()
    duration = data_size / float(sample_rate)

    # Read in sample data
    print(wave_file.getparams())

    # Close the file, as we don't need it any more
    wave_file.close()

    # Unpack the binary data into an array
    
   
    

    # Process many samples
    fouriers_per_second = 24  # Frames per second
    fourier_spread = 1.0 / fouriers_per_second
    fourier_width = fourier_spread
    fourier_width_index = fourier_width * float(sample_rate)
    length_to_process = int(duration) - 1
    
    
    #print ("Fourier width: %s" % str(fourier_width))
    
    total_transforms = int(round(length_to_process * fouriers_per_second))
    fourier_spacing = round(fourier_spread * float(sample_rate))
    
    print ("Duration: %s" % duration)
    print ("For Fourier width of " + str(fourier_width) +
           " need " + str(fourier_width_index) + " samples each FFT")
    print ("Doing " + str(fouriers_per_second) + " Fouriers per second")
    print ("Total " + str(total_transforms * fourier_spread))
    print ("Spacing: " + str(fourier_spacing))
    print ("Total transforms " + str(total_transforms))
    
    lastpoint = int(
        round(length_to_process * float(sample_rate) + fourier_width_index)) - 1

    sample_size = fourier_width_index
    freq = sample_rate / sample_size * np.arange(sample_size)

    def getBandWidth():
        return (2.0 / sample_size) * (sample_rate / 2.0)

    def freqToIndex(f):
        # If f (frequency is lower than the bandwidth of spectrum[0]
        if f < getBandWidth() / 2:
            return 0
        if f > (sample_rate / 2) - (getBandWidth() / 2):
            return sample_size - 1
        fraction = float(f) / float(sample_rate)
        index = round(sample_size * fraction)
        return index

    fft_averages = []

    def average_fft_bands(fft_array):
        num_bands = 12  # The number of frequency bands (12 = 1 octave)
        del fft_averages[:]
        for band in range(0, num_bands):
            avg = 0.0

            if band == 0:
                lowFreq = int(0)
            else:
                lowFreq = int(int(sample_rate / 2) /
                              float(2 ** (num_bands - band)))
            hiFreq = int((sample_rate / 2) /
                         float(2 ** ((num_bands - 1) - band)))
            lowBound = int(freqToIndex(lowFreq))
            hiBound = int(freqToIndex(hiFreq))
            for j in range(lowBound, hiBound):
                avg += fft_array[j]

            avg /= (hiBound - lowBound + 1)
            fft_averages.append(avg)
    input("Prass Enter To start,wear your headphone!!")

    space=int(terminalsize[0]/12)
    empty_string=" "*space
   
    wave_file=wave.open('ydlaudiodata.wav','r')
    p=pyaudio.PyAudio()
    chunk=2048
    stream = p.open(format =
                p.get_format_from_width(wave_file.getsampwidth()),
                channels = wave_file.getnchannels(),
                rate = wave_file.getframerate(),
                output = True)
    data = wave_file.readframes(chunk)
    print(wave_file.getparams())
    while data!='':
        stream.write(data)
        data = wave_file.readframes(chunk)
        #print(data,"\n")
        
        if sample_width==2:
            unpack_fmt = '%dh' %channel*chunk
        elif sample_width==1:
            unpack_fmt = '%db' %channel*chunk
        elif sample_width==4:
            unpack_fmt = '%di' %channel*chunk
        try:
            ori_sound_data = struct.unpack(unpack_fmt, data)
        except:
            quit()
        sound_data=[]
        #print(len(ori_sound_data))
        
        if channel==2:
            for i in range(int(len(ori_sound_data)/2)):
                sound_data.append(ori_sound_data[i*2])
        else:
            sound_data.append(ori_sound_data)
        
        fft_data = abs(np.fft.fft(sound_data))
        fft_data *= ((2**.5) / sample_size)
        average_fft_bands(fft_data)
        #print(fft_averages)####
        fft_normalize=[]        
        for i in fft_averages:
            max_height=int(i/terminalsize[1])
            if max_height>terminalsize[1]:
                max_height=terminalsize[1]
            fft_normalize.append(max_height)
        #print("  ",fft_normalize,"  ")
        word_line=""
        
        for i in range(terminalsize[1]+1):
            height=terminalsize[1]-i
            for j in range(len(fft_normalize)-1):
                if fft_normalize[j]<height:
                    word_line+=" "
                    word_line+=empty_string
                    if j==10:
                        word_line+="\n"
                else:  
                    word_line+="*"
                    word_line+=empty_string
                    if j==10:
                        word_line+="\n"
        print(word_line)
                        