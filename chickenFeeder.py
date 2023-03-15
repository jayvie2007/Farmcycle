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

relayChickenFeederOpen = 13 #violet
relayChickenFeederClose = 26 #blue


#Error Occur restart
def restart():
    os.execv(sys.executable,['python3'] + sys.argv)
#Error Occur restart

GPIO.setup(relayChickenFeederOpen, GPIO.OUT)
GPIO.setup(relayChickenFeederClose, GPIO.OUT)
GPIO.output(relayChickenFeederOpen, GPIO.OUT)
GPIO.output(relayChickenFeederClose, GPIO.OUT)
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
        feedChicken = db.child("FarmCycle").child("FeedChicken").get("")
        daysChicken = db.child("FarmCycle").child("DaysChicken").get("")
        chickenData = feedChicken.val()
        daysChickenData = daysChicken.val()
        delaaay = datetime.now().strftime('%H:%M %p')
        delaaay2 = datetime.now().strftime('%I:%M %p')
        chickenOutput = [chickenData[j] for j in chickenData]
        daysChickenOutput = [daysChickenData[j] for j in daysChickenData]
        FirstFeedTime = chickenOutput[0]
        ManualFeed = chickenOutput[1]
        SecondFeedTime = chickenOutput[2]
        chickenAge = daysChickenOutput[0]
        
        if ManualFeed == True:
            ManualFeed = False #set manual feed to false by updating firebase
            data = {
            "ManualFeed" : ManualFeed
            }
            db.child("FarmCycle").child("FeedChicken").update(data)
            status = True
            data = {
            "time" : delaaay2,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Manual Feed").update(data)
            GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
            GPIO.output(relayChickenFeederClose, GPIO.LOW)
            print("chicken feeding is on")
            time.sleep(3)   
            GPIO.output(relayChickenFeederOpen, GPIO.LOW)
            GPIO.output(relayChickenFeederClose, GPIO.HIGH)
            status = False
            data = {
            "time" : delaaay2,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Manual Feed").update(data)
            time.sleep(6)
            print("chicken feeding is off")
        elif FirstFeedTime == delaaay:
            if chickenAge <=14:
                status = False
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
            elif chickenAge <=15:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 15")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 15")
                time.sleep(60)
            elif chickenAge <=18:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 18")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(2)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 18")
                time.sleep(60)
            elif chickenAge <=21:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 21")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 21")
                time.sleep(60)
            elif chickenAge <=24:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 24")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(6)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 24")
                time.sleep(60)
            elif chickenAge <=27:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 27")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(8)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 27")
                time.sleep(60)
            elif chickenAge <=30:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 30")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(10)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 30")
                time.sleep(60)
            elif chickenAge <=33:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 33")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(12)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 33")
                time.sleep(60)
            elif chickenAge <=36:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 33")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(14)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 33")
                time.sleep(60)
            elif chickenAge <=36:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 36")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(16)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 36")
                time.sleep(60)
            elif chickenAge <=39:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 39")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(18)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 39")
                time.sleep(60)
            elif chickenAge <= 42:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 42")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(20)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 42")
                time.sleep(60)
            elif chickenAge >=43:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 36")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(22)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 36")
                time.sleep(60)
        elif SecondFeedTime == delaaay:
            if chickenAge <=14:
                status = False
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
            elif chickenAge <=15:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 15")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 15")
                time.sleep(60)
            elif chickenAge <=18:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 18")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(2)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 18")
                time.sleep(60)
            elif chickenAge <=21:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 21")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 21")
                time.sleep(60)
            elif chickenAge <=24:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 24")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(6)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 24")
                time.sleep(60)
            elif chickenAge <=27:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 27")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(8)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 27")
                time.sleep(60)
            elif chickenAge <=30:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 30")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(10)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 30")
                time.sleep(60)
            elif chickenAge <=33:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 33")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(12)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 33")
                time.sleep(60)
            elif chickenAge <=36:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 33")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(14)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 33")
                time.sleep(60)
            elif chickenAge <=36:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 36")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(16)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 36")
                time.sleep(60)
            elif chickenAge <=39:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 39")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(18)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 39")
                time.sleep(60)
            elif chickenAge <= 42:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 42")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(20)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 42")
                time.sleep(60)
            elif chickenAge >=43:
                status = True
                data = {
                "time" : delaaay2,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                print("chicken feeding is on age 43")
                time.sleep(4)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.LOW)
                time.sleep(22)
                GPIO.output(relayChickenFeederOpen, GPIO.LOW)
                GPIO.output(relayChickenFeederClose, GPIO.HIGH)
                print("chicken feeding is off age 43")
                time.sleep(60)
        else:
            print("waitingChickenFeeder")
            time.sleep(1)
    except:
        print("connectingChickenFeeder")
        restart()
        
        
