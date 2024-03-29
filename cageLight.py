import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime
import os
import sys
import time
import requests
relayLight = 14 #white 1st extension

url = "https://www.google.com"
timeout = 5
push = 1

#relay initialization
GPIO.setup(relayLight, GPIO.OUT)
GPIO.output(relayLight, GPIO.HIGH)
#relay initialization

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
time.sleep(2)
while True:
    try:
        timetoday = datetime.now().strftime('%x') #date today
        delaaay = datetime.now().strftime('%H:%M %p') #call real-time hour
        request = requests.get(url, timeout = timeout) #check if there is connection
        combinedString = timetoday + " " + delaaay

#Calling data from the firebase then convert it to array    
        cageControlInput = db.child("FarmCycle").child("CoolingSystemCage").get("")
        cageControlData = cageControlInput.val()
        cageControloutput = [cageControlData[j] for j in cageControlData]

        cageTempInput = db.child("FarmCycle").child("tCageTemp").get("")
        cageTempData = cageTempInput.val()
        cageTempOutput = [cageTempData[j] for j in cageTempData]

        cageLightAuto = cageControloutput[1]
        cageLightManual = cageControloutput[2]

        cageMax = int(cageTempOutput[0])
        cageMin = int(cageTempOutput[1])
        cageTemp = cageTempOutput[2]
#Calling data from the firebase then convert it to array

#Cage Light Auto
        if cageLightAuto == True:
            cagelightAutoStatus = True
            cageLightManual = ""

            LightManual = {
            "isLightManualOn" : cageLightManual
            }
            LightAutoStatus = {
            "status" : cagelightAutoStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(LightManual)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Light").update(LightAutoStatus)

            if push == 1:
                db.child("FarmCycle").child("HistoryLog").child("Temp").child("Cage Light").push(LightAutoStatus)
                push = 0
            elif cageTemp >= cageMax:
                print("The Cage light Auto is turned off")
                GPIO.output(relayLight, GPIO.HIGH)
            elif cageTemp <= cageMin:
                GPIO.output(relayLight, GPIO.LOW)
                print("The Cage light Auto is turned on")

        elif cageLightAuto == False:
            push = 1
            cagelightAutoStatus = False
            cageLightAuto = ""
            LightAuto = {
            "isCageLightOn" : cageLightAuto
            }
            LightAutoStatus = {
            "status" : cagelightAutoStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(LightAuto)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Light").update(LightAutoStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Cage Light").push(LightAutoStatus)
            GPIO.output(relayLight, GPIO.HIGH)
#Cage Light Auto

#Cage Light Manual
        elif cageLightManual == True:
            cagelightAutoStatus = False
            cagelightManualStatus = True

            cageLightAuto = ""
            data = {
            "isCageLightOn" : cageLightAuto
            }            
            LightManualStatus = {
            "status" : cagelightManualStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Light").update(LightManualStatus)

            if push == 1:
                db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Light").push(LightManualStatus)
                push = 0

            GPIO.output(relayLight, GPIO.LOW)  
            print("The Cage light is turned on")

        elif cageLightManual == False:
            push = 1
            cagelightManualStatus = False
            cageLightManual = ""
            LightManual = {
            "isLightManualOn" : cageLightManual
            }
            LightManualStatus = {
            "status" : cagelightManualStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(LightManual)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Light").update(LightManualStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Light").push(LightManualStatus)

            GPIO.output(relayLight, GPIO.HIGH)
            print("The Cage light is turned off")
        else:
            print("waitingCageLight")
            time.sleep(1)
#Cage Light Manual 
    except:
        print("connectingCageLight")