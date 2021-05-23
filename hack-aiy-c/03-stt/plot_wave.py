#!/usr/bin/python3
# https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

auf = sys.argv[1]
spf = wave.open(auf, 'r')

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

# If Stereo
if spf.getnchannels() > 2:
    print('Just mono files')
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave')
plt.plot(signal)
plt.show()

