#!/usr/bin/python3

import os
import sys
import time
from voice_engine.source import Source
from voice_engine.ec import EC
from voice_engine.kws import KWS

def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def main():
    src = Source(rate=16000, channels=1, frames_size=1600)
    ec = EC(channels=src.channels, capture=0, playback=2) 

    try:
        model = sys.argv[1]
        sens  = sys.argv[2]
        kws = KWS(model, sensitivity=float(sens))
        #kws = KWS(model='hi_lbj', sensitivity=0.65)

    except:
        kws = KWS()

    def on_detected(keyword):
        print('found {}'.format(keyword))
        play_audio_file("ding.wav")

    kws.on_detected = on_detected

    src.pipeline(ec, kws)

    src.pipeline_start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()


if __name__ == '__main__':
    main()
