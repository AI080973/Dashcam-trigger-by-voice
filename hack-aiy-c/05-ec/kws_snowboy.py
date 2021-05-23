#!/usr/bin/python3

import os
import sys
import time
from voice_engine.kws import KWS
from voice_engine.source import Source

def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def on_detected(keyword):
    print('found {}'.format(keyword))
    play_audio_file("ding.wav")

src = Source()
try:
    model = sys.argv[1]
    kws = KWS(model)
except:
    kws = KWS()
src.link(kws)

kws.on_detected = on_detected

kws.start()
src.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

kws.stop()
src.stop()
