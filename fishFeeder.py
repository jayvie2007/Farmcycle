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
        timetoday = datetime.now().strftime('%x') #date today
        delaaay = datetime.now().strftime('%H:%M %p') #call real-time hour
        request = requests.get(url, timeout = timeout) #check if there is connection
        combinedString = timetoday + " " + delaaay

#Calling data from the firebase then convert it to array   
        feedFish = db.child("FarmCycle").child("FeedFish").get("")
        fishData = feedFish.val()
        fishOutput = [fishData[j] for j in fishData]

        fishquanty = db.child("FarmCycle").child("FishQuantity").get("")
        daysFishData = fishquanty.val()
        fishquantityOutput = [daysFishData[j] for j in daysFishData]
        
        fishQuantity = int(fishquantityOutput[0])
        FirstFeedTime = fishOutput[0]
        ManualFeed = fishOutput[2]
        SecondFeedTime = fishOutput[3]
#Calling data from the firebase then convert it to array   

#Manual Feed
        if ManualFeed == True:
            status = True
            ManualFeed = False
            data = {
            "ManualFeed" : ManualFeed
            }
            mFeed = {
            "time" : combinedString,
            "status" : status
            }
            db.child("FarmCycle").child("FeedFish").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Manual Feed").update(mFeed)
            db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish Manual Feed").push(mFeed)

            GPIO.output(relayFishFeederOpen, GPIO.HIGH)
            GPIO.output(relayFishFeederClose, GPIO.LOW)
            print("Fish feeder is opening")
            time.sleep(3)
            GPIO.output(relayFishFeederClose, GPIO.HIGH)
            GPIO.output(relayFishFeederOpen, GPIO.LOW)
            time.sleep(6)
            print("Fish feeder is closing")
                    
            status = False
            mFeed = {
            "time" : combinedString,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Manual Feed").update(mFeed)
            db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish Manual Feed").push(mFeed)
#Manual Feed
 
#Auto Feed        
        elif FirstFeedTime == delaaay:
            if fishQuantity == 0:
                status = False
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
                #db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish First Feeding").push(data)
            
            elif fishQuantity <=5:
                status = True
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish First Feeding").push(data)
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
                #db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish Second Feeding").push(data)

            elif fishQuantity <=5:
                status = True
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Fish").child("Fish Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Fish").child("Fish Second Feeding").push(data)
                
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
#Auto Feed
    except:
        print("connectingFishFeeder")
        restart()