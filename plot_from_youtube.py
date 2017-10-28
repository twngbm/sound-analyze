#import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import time
import math
sr = 44100
re_sample_rate=10
f=9049088
total_dot=f*re_sample_rate/sr
re_sample_dot=int(sr/re_sample_rate)
with open('filedata.out','r') as files:
    line=list(files)
    #print(len(line))
    for i in range(int(total_dot)):
        x=re_sample_dot*i
        #print(x)
        #print(line[x].find(" "))
        out=int(math.log(abs(int(line[x][:line[x].find(" ")]))+1,2))
        print("\n"*22)
        print("x"*out)
        time.sleep(1/re_sample_rate)
        #print(i)
files.close()
'''
spf = wave.open('h.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#If Stereo
if spf.getnchannels() == 2:
    print 'Just mono files'
    sys.exit(0)
print type(signal)
plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()
'''