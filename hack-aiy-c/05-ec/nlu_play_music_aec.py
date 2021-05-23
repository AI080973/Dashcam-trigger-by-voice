#!/usr/bin/python3
# python3 nlu_play_music_aec.py 0.65
# alsactl --file ~/.config/asound.state restore
# alsactl --file ~/.config/asound.state store

import uuid
import os
import sys
import signal
import speech_recognition as sr
import urllib
import uuid
import json
import requests
import time    
import subprocess
import configparser
import os
import RPi.GPIO as GPIO
from gtts import gTTS
from pygame import mixer
import tempfile
import threading

from voice_engine.source import Source
from voice_engine.ec import EC
from voice_engine.kws import KWS

interrupted = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)

config = configparser.ConfigParser()
config.read('../smart_speaker.conf')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('dialogflow', 'google_app_credential')
project_id = config.get('dialogflow', 'project_id')
session_id = str(uuid.uuid4())
language_code = 'zh-TW'


def speak(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('tts.mp3')
        mixer.init()
        mixer.music.load('tts.mp3')
        mixer.music.play(1)
        time.sleep( int(len(sentence)/2) )
        os.remove('tts.mp3')


def audioRecorderCallback():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) 
        GPIO.output(25, GPIO.HIGH)
        print('Say something>>> ')
        audio=r.listen(source)
        GPIO.output(25, GPIO.LOW)

    print("converting audio to text")

    try:
        texts = r.recognize_google(audio, language="zh-TW")
        print(texts)

        import dialogflow_v2 as dialogflow
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        print('Session path: {}'.format(session))

        text_input = dialogflow.types.TextInput(
            text=texts, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}'.format(
            response.query_result.fulfillment_text))

        fulfillment = response.query_result.fulfillment_text
        singer = fulfillment.split(' ')[1]
        song = fulfillment.split(' ')[2]
        query = '"{} {}"'.format(singer, song)

        sentence = '現在正要播放' + singer + '的' + song
        th = threading.Thread(target=speak, args=(sentence,'zh-tw',))
        th.start()

        exit_code = subprocess.call("python3 yt3.py " + query, shell=True)

    except IndexError:
        if len(response.query_result.fulfillment_text) == 0:
            sentence = '我聽不懂你說的話，請再說一次'
            th = threading.Thread(target=speak, args=(sentence,'zh-tw',))
            th.start()
        else:
            speak(response.query_result.fulfillment_text, 'zh-tw')

        pass

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")


def main():
    src = Source(rate=16000, channels=1, frames_size=1600)
    ec = EC(channels=src.channels, capture=0, playback=2) 

    def on_detected(keyword):
        print('found {}'.format(keyword))
        play_audio_file("ding.wav")

        try:
            subprocess.call("kill -9 `ps aux | grep python3 | grep yt3.py | awk '{print $2}'`", shell=True)
        finally:
            th = threading.Thread(target=audioRecorderCallback, args=())
            th.start()


    try:
        model = sys.argv[1]
        sens  = sys.argv[2]
        kws = KWS(model, sensitivity=float(sens))
        #kws = KWS(model='hi_lbj', sensitivity=0.65)

    except:
        sens  = sys.argv[1]
        kws = KWS(sensitivity=float(sens))
        print("sens: ", sens)


    kws.on_detected = on_detected
    src.pipeline(ec, kws)
    src.pipeline_start()

    try:
        while True:
            time.sleep(0.1)
    except Exception as e: 
        print(e)
    finally:
        GPIO.cleanup()

    src.pipeline_stop()


if __name__ == '__main__':
    main()
