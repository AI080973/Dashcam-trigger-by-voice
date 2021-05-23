#!/usr/bin/python3

import time
from gtts import gTTS
from pygame import mixer
import tempfile

def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(loops)

sentence = 'Hello World'
speak(sentence, 'en')
time.sleep(int(len(sentence)/2 ))

sentence = '現在溫度是 31 度'
speak(sentence, 'zh-tw')
time.sleep(int(len(sentence)/2 ))
