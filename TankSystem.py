import RPi.GPIO as GPIO
import board
import pyrebase
from datetime import datetime
import time
import os
import sys
import requests

url = "https://www.google.com"
timeout = 5
#FIREBASE 18 23 25
relayHeater = 18 #blue 4th extension
relayPumpIn = 25 #yellow 6th extension
relayPumpOut = 23 #green 3rd extension

#relay initialization
GPIO.setup(relayHeater, GPIO.OUT)
GPIO.output(relayHeater, GPIO.HIGH)
GPIO.setup(relayPumpIn, GPIO.OUT) #water in
GPIO.output(relayPumpIn, GPIO.HIGH)
GPIO.setup(relayPumpOut, GPIO.OUT) #water out
GPIO.output(relayPumpOut, GPIO.HIGH)
#relay initialization

#Error Occur restart
def restart():
    os.execv(sys.executable,['python3'] + sys.argv)
#Error Occur restart

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
        heaterInput = db.child("FarmCycle").child("CoolingSystemTank").get("")
        heaterData = heaterInput.val()
        heateroutput = [heaterData[j] for j in heaterData]

        tankTempInput = db.child("FarmCycle").child("tTankTemp").get("")
        tankTempData = tankTempInput.val()
        tankTempOutput = [tankTempData[j] for j in tankTempData]
        
        waterLevelInput = db.child("FarmCycle").child("WaterLevel").get("")
        waterLevelData = waterLevelInput.val()
        waterLeveloutput = [waterLevelData[j] for j in waterLevelData]
        
        isManualHeaterOnTank = heateroutput[0]
        isPumpInOn = heateroutput[1]
        isPumpOutOn = heateroutput[2]
        isTankHeaterOn = heateroutput[3]

        tankMax = tankTempOutput[0]
        tankMin = tankTempOutput[1]
        tankTemp = tankTempOutput[2]
        
        waterLevel = int(waterLeveloutput[0])
#Calling data from the firebase then convert it to array  

#Auto Controller of Heater
        if isTankHeaterOn == True:
            isTankHeaterOnStatus = True
            isManualHeaterOnTankStatus = False
            isManualHeaterOnTank = False
            ManualHeater = {
            "isManualHeaterOnTank" : isManualHeaterOnTank,
            }
            ManualHeaterStatus = {
            "status" : isManualHeaterOnTankStatus,
            "time" : combinedString
            }
            TankHeaterStatus = {
            "status" : isTankHeaterOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemTank").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Heater").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Heater System").update(data)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Heater").push(data)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Heater System").push(data)

            if tankTemp <= tankMin:
                GPIO.output(relayHeater, GPIO.LOW)
                print("The Heater is turned on")
            elif tankTemp >= tankMax:
                GPIO.output(relayHeater, GPIO.HIGH)
                print("The Heater is turned off")

        elif isTankHeaterOn == False:
            isTankHeaterOn = ""
            isTankHeaterOnStatus = False
            TankHeater = {
            "isTankHeaterOn" : isTankHeaterOn,
            }
            TankHeaterStatus = {
            "status" : isTankHeaterOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemTank").update(TankHeater)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Heater System").update(TankHeaterStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Heater System").push(TankHeaterStatus)
            
            print("The auto heater is offline")            
            
#Auto Controller of Heater

#Manual Controller of Heater
        elif isManualHeaterOnTank == True:
            isManualHeaterOnTankStatus = True
            isTankHeaterOnStatus = False
            ManualHeaterStatus = {
            "status" : isManualHeaterOnTankStatus,
            "time" : combinedString
            }
            TankHeaterStatus = {
            "status" : isTankHeaterOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Heater System").update(ManualHeaterStatus)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Heater").update(TankHeaterStatus)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Heater System").push(ManualHeaterStatus)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Heater").push(TankHeaterStatus)

            GPIO.output(relayHeater, GPIO.LOW)
            print("The Heater is turned on")

        elif isManualHeaterOnTank == False:
            isManualHeaterOnTankStatus = False
            isManualHeaterOnTank = ""
            data = {
            "isManualHeaterOnTank" : isManualHeaterOnTank
            }
            ManualHeaterStatus = {
            "status" : isManualHeaterOnTankStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemTank").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Manual Heater").update(ManualHeaterStatus)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Manual Heater").push(ManualHeaterStatus)

            GPIO.output(relayHeater, GPIO.HIGH)
            print("The Heater is turned off")
               
#Manual Controller of Heater

#Manual Controller of Pump In
        elif isPumpInOn == True:
            isPumpInOnStatus = True
            data = {
            "status" : isPumpInOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Pump In").update(data)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Pump In").push(data)

            GPIO.output(relayPumpIn, GPIO.LOW)
            print("The Pump In is turned on")
        elif isPumpInOn == False:
            isPumpInOnStatus = False
            isPumpInOn = ""
            data = {
            "isPumpInOn" : isPumpInOn
            }
            PumpInData = {
            "status" : isPumpInOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemTank").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Pump In").update(PumpInData)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Pump In").push(PumpInData)
            
            GPIO.output(relayPumpIn, GPIO.HIGH)
            print("The Pump In is turned off")
#Manual Controller of Pump In

#Manual Controller of Pump Out
        elif isPumpOutOn == True:
            isPumpOutOnStatus = True
            data = {
            "status" : isPumpOutOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Pump Out").update(data)
            #db.child("FarmCycle").child("HistoryLog").child("Temp").child("Pump Out").push(data)
            
            GPIO.output(relayPumpOut, GPIO.LOW)
            print("The PumpOut is turned on")

        elif isPumpOutOn == False:
            isPumpOutOnStatus = False
            isPumpOutOn = ""
            data = {
            "isPumpOutOn" : isPumpOutOn
            }
            PumpOutData = {
            "status" : isPumpOutOnStatus,
            "time" : combinedString
            }
            db.child("FarmCycle").child("CoolingSystemTank").update(data)
            db.child("FarmCycle").child("ActivityLog").child("Temp").child("Pump Out").update(PumpOutData)
            db.child("FarmCycle").child("HistoryLog").child("Temp").child("Pump Out").push(PumpOutData)
            GPIO.output(relayPumpOut, GPIO.HIGH)
            print("The PumpOut is turned off")
            
        else:
            print("waitingTankSystem")
            time.sleep(1)
#Manual Controller of Pump Out
    except:
        print("connectingTankSystem")
        restart()
