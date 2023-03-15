import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime


#relayPlantLight = 18 #purple 3rd extension orig
relayPlantLight = 24 #purple 3rd extension

#relay initialization
GPIO.setup(relayPlantLight, GPIO.OUT)
GPIO.output(relayPlantLight, GPIO.HIGH)
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

while True:
    currentTime = datetime.now().strftime('%H:%M')
    plantControlInput = db.child("FarmCycle").child("PlantsLight").get("")
    plantControlData = plantControlInput.val()
    plantControloutput = [plantControlData[j] for j in plantControlData]
    
    plantOff = plantControloutput[0]
    plantOn = plantControloutput[1]
    plantLightAuto = plantControloutput[2]
    plantLight = plantControloutput[3]
    

#Plant Auto Control
    if plantLightAuto == True:
        plantLight = False #set manual plant light to false by updating firebase
        data = {
        "isLightOn" : plantLight
        }
        db.child("FarmCycle").child("PlantsLight").update(data)
        if currentTime == plantOff:
            GPIO.output(relayPlantLight, GPIO.HIGH)
            print("The Plant light Auto is turned off")
        elif currentTime == plantOn:
            GPIO.output(relayPlantLight, GPIO.LOW)
            print("The Plant light Auto is turned on")
    elif plantLightAuto == False:
        plantLightAuto = ""
        GPIO.output(relayPlantLight, GPIO.HIGH)
        data = {
        "isAutoOn" : plantLightAuto
        }
        db.child("FarmCycle").child("PlantsLight").update(data)
        GPIO.output(relayPlantLight, GPIO.HIGH)
#Plant Auto Control

#Plant Manual Control        
    elif plantLight == True:
        GPIO.output(relayPlantLight, GPIO.LOW)
        print("The Plant light is turned on")
    elif plantLight == False:
        GPIO.output(relayPlantLight, GPIO.HIGH)
        print("The Plant light is turned off")
#Plant Manual Control     
