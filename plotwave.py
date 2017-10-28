#import matplotlib.pyplot as plt
#import numpy as np
import wave
#import sys\
import time

with open('filedata.out','r') as files:
    line=list(files)
    print(len(line))
    for i in range(int(44100/4)):
        print(line[i][:-1])
        time.sleep(0.25)
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