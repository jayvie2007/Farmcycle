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
push = 1

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
        timetoday = datetime.now().strftime('%x') #date today
        delaaay = datetime.now().strftime('%H:%M %p') #call real-time hour
        request = requests.get(url, timeout = timeout) #check if there is connection
        combinedString = timetoday + " " + delaaay

#Calling data from the firebase then convert it to array   
        feedChicken = db.child("FarmCycle").child("FeedChicken").get("")
        chickenData = feedChicken.val()
        chickenOutput = [chickenData[j] for j in chickenData]

        daysChicken = db.child("FarmCycle").child("DaysChicken").get("")
        daysChickenData = daysChicken.val()
        daysChickenOutput = [daysChickenData[j] for j in daysChickenData]
        
        FirstFeedTime = chickenOutput[0]
        ManualFeed = chickenOutput[1]
        SecondFeedTime = chickenOutput[2]

        chickenAge = daysChickenOutput[0]
 #Calling data from the firebase then convert it to array          
        
 #Manual Feeder       
        if ManualFeed == True:
            ManualFeed = False
            status = True
            data = {
            "ManualFeed" : ManualFeed
            }
            mFeed = {
            "time" : combinedString,
            "status" : status
            }
            db.child("FarmCycle").child("FeedChicken").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Manual Feed").update(mFeed)
            db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Manual Feed").push(mFeed)
            
            GPIO.output(relayChickenFeederOpen, GPIO.HIGH)
            GPIO.output(relayChickenFeederClose, GPIO.LOW)
            print("chicken feeding is on")
            time.sleep(3)   
            GPIO.output(relayChickenFeederOpen, GPIO.LOW)
            GPIO.output(relayChickenFeederClose, GPIO.HIGH)
            time.sleep(6)
            print("chicken feeding is off")

            push = 1
            status = False
            mFeed = {
            "time" : combinedString,
            "status" : status
            }
            db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Manual Feed").update(mFeed)
            db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Manual Feed").push(mFeed)
#Manual Feeder

#Auto Feeder            
        elif FirstFeedTime == delaaay:
            if chickenAge <=14:
                status = False
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                if push == 1:
                    push = 0
                    db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
            
            elif chickenAge <=15:
                status = True
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
            
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)

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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken First Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken First Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                if push == 1:
                    push = 0
                    db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
            
            elif chickenAge <=15:
                status = True
                data = {
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)

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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
               
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)

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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)

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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)
                
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
                "time" : combinedString,
                "status" : status
                }
                db.child("FarmCycle").child("ActivityLog").child("Chicken").child("Chicken Second Feeding").update(data)
                db.child("FarmCycle").child("HistoryLog").child("Chicken").child("Chicken Second Feeding").push(data)

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
#Auto Feeder 
    except:
        print("connectingChickenFeeder")
        restart()
        
        
