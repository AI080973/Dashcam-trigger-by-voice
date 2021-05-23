#!/usr/bin/python3

import RPi.GPIO as GPIO
import time    

GPIO.setmode(GPIO.BCM)
LED_PIN = 25    
GPIO.setup(LED_PIN, GPIO.OUT)

print("LED is on")
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(3)

GPIO.cleanup()
