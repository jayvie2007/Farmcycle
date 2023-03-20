import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime
import os
import time
import sys
import requests
relayFan = 15 #gray 2nd extension

url = "https://www.google.com"
timeout = 5
push = 1

#Error Occur restart
def restart():
    os.execv(sys.executable,['python3'] + sys.argv)
#Error Occur restart

#relay initialization
GPIO.setup(relayFan, GPIO.OUT)
GPIO.output(relayFan, GPIO.HIGH)
#relay initialization

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
time.sleep(3)
while True:
    try:
        timetoday = datetime.now().strftime('%x') #date today
        delaaay = datetime.now().strftime('%H:%M %p') #call real-time hour
        request = requests.get(url, timeout = timeout) #check if the raspberry has connection
        combinedString = timetoday + " " + delaaay

#Calling data from the firebase then convert it to array    
        cageControlInput = db.child("FarmCycle").child("CoolingSystemCage").get("")
        cageControlData = cageControlInput.val()
        cageControloutput = [cageControlData[j] for j in cageControlData]

        cageTempInput = db.child("FarmCycle").child("tCageTemp").get("")
        cageTempData = cageTempInput.val()
        cageTempOutput = [cageTempData[j] for j in cageTempData]

        cageFanAuto = cageControloutput[0]
        cageFanManual = cageControloutput[3]
        
        cageMax = int(cageTempOutput[0])
        cageMin = int(cageTempOutput[1])
        cageTemp = cageTempOutput[2]
#Calling data from the firebase then convert it to array
        
#Cage Fan Auto
        if cageFanAuto == True:
            CageFanAutoStatus = True
            CageFanManualStatus = False
            cageFanManual = False
            FanManual = {
            "isManualFanOnCage" : cageFanManual 
            }
            FanAutoStatus = {
            "status" : CageFanAutoStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(FanManual)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Fan").update(FanAutoStatus)
                 
            if push == 1:
                push = 0
                db.child("FarmCycle").child("HistoryLog").child("Temp").child("Cage Fan").push(FanAutoStatus)
            elif cageTemp <= cageMin:
                GPIO.output(relayFan, GPIO.HIGH)
                print("The Cage fan auto is turned off")
            elif cageTemp >= cageMax:
                GPIO.output(relayFan, GPIO.LOW)
                print("The Cage fan auto is turned on")

        elif cageFanAuto == False:
            push = 1
            CageFanAutoStatus = False
            cageFanAuto = ""
            FanAuto = {
            "isCageFanOn" : cageFanAuto,
            }
            FanAutoStatus = {
            "status" : CageFanAutoStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(FanAuto)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Fan").update(FanAutoStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Cage Fan").push(FanManualStatus)
            GPIO.output(relayFan, GPIO.HIGH)
#Cage Fan Auto

#Cage Fan Manual
        elif cageFanManual == True:
            CageFanAutoStatus = False
            CageFanManualStatus = True
            cageFanAuto = ""
            FanAutoStatus = {
            "status" : CageFanAutoStatus,
            "time" : combinedString
            }
            FanManualStatus = {
            "status" : CageFanManualStatus,
            "time" : combinedString
            }  
            FanAuto = {
            "isCageFanOn" : cageFanAuto,
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Fan").update(FanManualStatus) 
            db.child("FarmCycle").child("CoolingSystemCage").update(FanAuto)

            if push == 1:
                push = 0
                db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Fan").push(FanManualStatus)
            
            GPIO.output(relayFan, GPIO.LOW)  
            print("The Cage fan is turned on")

        elif cageFanManual == False:
            push = 1
            CageFanManualStatus = False
            cageFanManual = ""
            FanManualStatus = {
            "status" : CageFanManualStatus,
            "time" : combinedString
            }   
            FanManual = {
            "isManualFanOnCage" : cageFanManual
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(FanManual)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Fan").update(FanManualStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Fan").push(FanManual)
            
            GPIO.output(relayFan, GPIO.HIGH)
            print("The Cage fan is turned off")
        else:
            print("waitingCageFan")
#Cage Fan Manuals
    except:
        print("connectingCageFan")
        restart()