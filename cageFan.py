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
        delaaay = datetime.now().strftime('%I:%M %p')
        request = requests.get(url, timeout = timeout)
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
            cageFanManual = False #set auto cage light to false by updating firebase
            data = {
            "isManualFanOnCage" : cageFanManual 
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(data)
            data = {
            "status" : CageFanAutoStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Fan").update(data)
            data = {
            "status" : CageFanManualStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Fan").update(data)      
            
            if cageTemp <= cageMin:
                GPIO.output(relayFan, GPIO.HIGH)
                print("The Cage fan auto is turned off")
            elif cageTemp >= cageMax:
                GPIO.output(relayFan, GPIO.LOW)
                print("The Cage fan auto is turned on")
        elif cageFanAuto == False:
            CageFanAutoStatus = False
            cageFanAuto = ""
            data = {
            "isCageFanOn" : cageFanAuto,
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(data)
            data = {
            "status" : CageFanAutoStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Fan").update(data)
            GPIO.output(relayFan, GPIO.HIGH)
    #Cage Fan Auto

    #Cage Fan Manual
        elif cageFanManual == True:
            CageFanAutoStatus = False
            CageFanManualStatus = True
            cageFanAuto = "" #set auto cage light to false by updating firebase
            data = {
            "status" : CageFanAutoStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Cage Fan").update(data)
            data = {
            "status" : CageFanManualStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Fan").update(data)   
            data = {
            "isCageFanOn" : cageFanAuto,
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(data)
            GPIO.output(relayFan, GPIO.LOW)  
            print("The Cage fan is turned on")
        elif cageFanManual == False:
            CageFanManualStatus = False
            data = {
            "status" : CageFanManualStatus,
            "time" : delaaay
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Fan").update(data)   
            GPIO.output(relayFan, GPIO.HIGH)
            print("The Cage fan is turned off")
            cageFanManual = "" #set manual feed to false by updating firebase
            data = {
            "isManualFanOnCage" : cageFanManual
            }
            db.child("FarmCycle").child("CoolingSystemCage").update(data)
        else:
            print("waitingCageFan")
    #Cage Fan Manuals
    except:
        print("connectingCageFan")
        restart()