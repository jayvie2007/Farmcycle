import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime
import os
import time
import sys
import requests

#relayPlantLight = 18 #purple 3rd extension orig
relayPlantLight = 24 #purple 3rd extension

#relay initialization
GPIO.setup(relayPlantLight, GPIO.OUT)
GPIO.output(relayPlantLight, GPIO.HIGH)
#relay initialization

url = "https://www.google.com"
timeout = 5
push = 1

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
        request = requests.get(url, timeout = timeout) #check if the raspberry has connection
        combinedString = timetoday + " " + delaaay

#Calling data from the firebase then convert it to array  
        currentTime = datetime.now().strftime('%H:%M')
        plantControlInput = db.child("FarmCycle").child("PlantsLight").get("")
        plantControlData = plantControlInput.val()
        plantControloutput = [plantControlData[j] for j in plantControlData]
        
        plantOff = plantControloutput[0]
        plantOn = plantControloutput[1]
        plantLightAuto = plantControloutput[2]
        plantLight = plantControloutput[3]
#Calling data from the firebase then convert it to array          

#Plant Auto Control
        if plantLightAuto == True:
            plantLight = False
            plantLightOn = True

            data = {
            "isLightOn" : plantLight
            }
            plantLightStatus = {
            "status" : plantLightOn,
            "time" : combinedString
            }  
            db.child("FarmCycle").child("PlantsLight").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Plant").child("Plant Light").update(plantLightStatus)
            
            if push == 1:
                push = 0
                db.child("FarmCycle").child("HistoryLog").child("Plant").child("Plant Light").push(plantLightStatus)
            elif currentTime == plantOff:
                GPIO.output(relayPlantLight, GPIO.HIGH)
                print("The Plant light Auto is turned off")
            elif currentTime == plantOn:
                GPIO.output(relayPlantLight, GPIO.LOW)
                print("The Plant light Auto is turned on")

        elif plantLightAuto == False:
            plantLightAuto = ""
            plantLight = False
            push = 1

            data = {
            "isAutoOn" : plantLightAuto
            }
            plantLightStatus = {
            "status" : plantLight,
            "time" : combinedString
            }  
            db.child("FarmCycle").child("PlantsLight").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Plant").child("Plant Light").update(plantLightStatus)
            db.child("FarmCycle").child("HistoryLog").child("Plant").child("Plant Light").push(plantLightStatus)

            GPIO.output(relayPlantLight, GPIO.HIGH)
            print("The plant light auto is off")
#Plant Auto Control

#Plant Manual Control        
        elif plantLight == True:
            plantlightManual = True
            plantLightAutoStatus = False
            data = {
            "isAutoOn" : plantLightAutoStatus
            }
            plantLightStatus = {
            "status" : plantlightManual,
            "time" : combinedString
            }
            db.child("FarmCycle").child("PlantsLight").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Plant").child("Plant Light").update(plantLightStatus)

            if push == 1:
                push = 0
                db.child("FarmCycle").child("HistoryLog").child("Plant").child("Plant Light").push(plantLightStatus)

            GPIO.output(relayPlantLight, GPIO.LOW)
            print("The Plant light is turned on")
        
        elif plantLight == False:
            push = 1
            plantLight = ""
            plantlightManual = False

            data = {
            "isLightOn" : plantLight
            }
            plantLightStatus = {
            "status" : plantlightManual,
            "time" : combinedString
            }  
            db.child("FarmCycle").child("PlantsLight").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Plant").child("Plant Light").update(plantLightStatus)
            db.child("FarmCycle").child("HistoryLog").child("Plant").child("Plant Light").push(plantLightStatus)

            GPIO.output(relayPlantLight, GPIO.HIGH)
            print("The Plant light is turned off")
#Plant Manual Control     
    except:
        print("connectingCageFan")
        restart()
