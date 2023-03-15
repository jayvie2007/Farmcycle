import RPi.GPIO as GPIO
import board
import pyrebase
import time
from datetime import datetime
import os
import sys
import requests

url = "https://www.google.com"
timeout = 5

relayFishFeederOpen = 16 #orange
relayFishFeederClose = 20 #red
GPIO.setup(relayFishFeederOpen, GPIO.OUT)
GPIO.setup(relayFishFeederClose, GPIO.OUT)
GPIO.output(relayFishFeederOpen, GPIO.OUT)
GPIO.output(relayFishFeederClose, GPIO.OUT)


#Error Occur restart
def restart():
    os.execv(sys.executable,['python3'] + sys.argv)
#Error Occur restart

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
while True:
    try:
        request = requests.get(url, timeout = timeout)
        feedFish = db.child("FarmCycle").child("FeedFish").get("")
        fishquanty = db.child("FarmCycle").child("FishQuantity").get("")
        fishData = feedFish.val()
        daysFishData = fishquanty.val()
        delaaay = datetime.now().strftime('%H:%M %p')
        delaaay2 = datetime.now().strftime('%I:%M %p')
        fishOutput = [fishData[j] for j in fishData]
        fishquantityOutput = [daysFishData[j] for j in daysFishData]
        FirstFeedTime = fishOutput[0]
        ManualFeed = fishOutput[2]
        SecondFeedTime = fishOutput[3]
        fishQuantity = int(fishquantityOutput[0])

        if ManualFeed == True:
            status = True
            data = {
            "time" : delaaay2,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Manual Feed").update(data)
            GPIO.output(relayFishFeederOpen, GPIO.HIGH)
            GPIO.output(relayFishFeederClose, GPIO.LOW)
            print("Fish feeder is opening")
            time.sleep(3)
            GPIO.output(relayFishFeederClose, GPIO.HIGH)
            GPIO.output(relayFishFeederOpen, GPIO.LOW)
            time.sleep(6)
            print("Fish feeder is closing")
            ManualFeed = False #set manual feed to false by updating firebase
            data = {
            "ManualFeed" : ManualFeed
            }
            #firebase name
            db.child("FarmCycle").child("FeedFish").update(data)
            status = False
            data = {
            "time" : delaaay2,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Manual Feed").update(data)
        elif FirstFeedTime == delaaay:
            if fishQuantity == 0:
                status = False
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
            elif fishQuantity <=5:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
                GPIO.output(relayFishFeederOpen, GPIO.HIGH)
                GPIO.output(relayFishFeederClose, GPIO.LOW)
                print("Fish feeder is opening")
                time.sleep(2)
                GPIO.output(relayFishFeederOpen, GPIO.LOW)
                GPIO.output(relayFishFeederClose, GPIO.HIGH)
                print("Fish feeder is closing")
                time.sleep(60)
            elif fishQuantity >=6:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
                GPIO.output(relayFishFeederOpen, GPIO.HIGH)
                GPIO.output(relayFishFeederClose, GPIO.LOW)
                print("Fish feeder is opening")
                time.sleep(3)
                GPIO.output(relayFishFeederOpen, GPIO.LOW)
                GPIO.output(relayFishFeederClose, GPIO.HIGH)
                print("Fish feeder is closing")
                time.sleep(60)
        elif SecondFeedTime == delaaay:
            if fishQuantity == 0:
                status = False
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
            elif fishQuantity <=5:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
                GPIO.output(relayFishFeederOpen, GPIO.HIGH)
                GPIO.output(relayFishFeederClose, GPIO.LOW)
                print("Fish feeder is opening")
                time.sleep(2)
                GPIO.output(relayFishFeederOpen, GPIO.LOW)
                GPIO.output(relayFishFeederClose, GPIO.HIGH)
                print("Fish feeder is closing")
                time.sleep(60)
            elif fishQuantity >=6:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
                GPIO.output(relayFishFeederOpen, GPIO.HIGH)
                GPIO.output(relayFishFeederClose, GPIO.LOW)
                print("Fish feeder is opening")
                time.sleep(3)
                GPIO.output(relayFishFeederOpen, GPIO.LOW)
                GPIO.output(relayFishFeederClose, GPIO.HIGH)
                print("Fish feeder is closing")
                time.sleep(60)
        else:
            print("waitingFishFeeder")
            time.sleep(1)
    except:
        print("connectingFishFeeder")
        restart()