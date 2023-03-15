import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import pyrebase

import os
import sys
import requests

from time import sleep, strftime
from datetime import datetime

url = "https://www.google.com"
timeout = 5
#FIREBASE
config = {
    "apiKey": "AIzaSyDeWWny9C3G9T7s4bUqaJROstQzKeEsfwA",
    "authDomain": "farmcycle-9ccea.firebaseapp.com",
    "databaseURL": "https://farmcycle-9ccea-default-rtdb.firebaseio.com",
    "projectId?": "farmcycle-9ccea",
    "storageBucket": "farmcycle-9ccea.appspot.com",
    "messagingSenderId": "801074370409",
    "appId": "1:801074370409:web:f2d3ab80719c5c63bb8ff8",
    "measurementId": "G-ML38MSWY1S"

    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#FIREBASE

#DHT22
dht = adafruit_dht.DHT22(board.D21)
dht = adafruit_dht.DHT22(board.D21, use_pulseio=False)
#DHT22

#Error Occur restart
def restart():
    os.execv(sys.executable,['python3'] + sys.argv)
#Error Occur restart

while True:
    try:
        request = requests.get(url, timeout = timeout)
        temperature = dht.temperature
        temp = ("T:{:.1f}".format(temperature))
        print("T:{:.1f}".format(temperature))

        data = {
        "Temp" : temperature,
        }
        #firebase name
        db.child("FarmCycle").child("tCageTemp").update(data)
        time.sleep(1)
               
    except RuntimeError as e:
        print("Reading from DHT failure: ", e.args)
        time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Stopped")
    except:
        print("connecting")
        restart()
