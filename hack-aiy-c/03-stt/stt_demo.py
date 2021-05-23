#!/usr/bin/python3

import sys 
import speech_recognition as sr
import RPi.GPIO as GPIO
import time    

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

r = sr.Recognizer() 
r.dynamic_energy_threshold = True
r.pause_threshold = 1
r.phrase_threshold = 0.3
r.non_speaking_duration = 0.5

with sr.Microphone() as source:
    #print("Please wait. Calibrating microphone...") 
    r.adjust_for_ambient_noise(source, duration=1) 
    print('Say something>>> ')
    GPIO.output(25, GPIO.HIGH)
    audio=r.listen(source, timeout=3)
    GPIO.output(25, GPIO.LOW)

try:
    print('Google Speech Recognition thinks you said:')
    sent = r.recognize_google(audio, language="zh-TW")
    print("{}".format(sent))
except sr.UnknownValueError:
    print('Google Speech Recognition could not understand audio')
except sr.RequestError as e:
    print('No response from Google Speech Recognition service: {0}'.format(e))

GPIO.cleanup()

