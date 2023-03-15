import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime
import time
#FIREBASE

relayFanOne = 8 #orange 7th extension
relayFanTwo = 7 #red 8th extension
relayOff = 24

#relay initialization
GPIO.setup(relayFanOne, GPIO.OUT)
GPIO.setup(relayFanTwo, GPIO.OUT)
GPIO.output(relayFanOne, GPIO.HIGH)
GPIO.output(relayFanTwo, GPIO.HIGH)
GPIO.setup(relayOff, GPIO.OUT)
GPIO.output(relayOff, GPIO.HIGH)
#relay initialization
time.sleep(7)
while True:
    GPIO.output(relayFanTwo, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(relayFanOne, GPIO.LOW)
    time.sleep(1200)
    GPIO.output(relayFanOne, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(relayFanTwo, GPIO.LOW)
    time.sleep(1200)

