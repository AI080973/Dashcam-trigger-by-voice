#!/usr/bin/python3

import uuid
import os
import sys
import snowboydecoder
import signal
import speech_recognition as sr
import urllib
import uuid
import json
import requests
import time    
import subprocess
import configparser

interrupted = False

config = configparser.ConfigParser()
config.read('../../smart_speaker.conf')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('dialogflow', 'google_app_credential')
project_id = config.get('dialogflow', 'project_id')
session_id = str(uuid.uuid4())
language_code = 'zh-TW'


def audioRecorderCallback(fname):
    print("converting audio to text")
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.5
    with sr.AudioFile(fname) as source:
        r.adjust_for_ambient_noise(source, duration=1) 
        audio = r.record(source)  # read the entire audio file
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
        exit_code = subprocess.call("python3 yt3.py " + query, shell=True)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    finally:
        os.remove(fname)


def detectedCallback():
    snowboydecoder.play_audio_file()
    sys.stdout.write("Say something>>> ")
    sys.stdout.flush()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print("Listening... Press Ctrl+C to exit")

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()

