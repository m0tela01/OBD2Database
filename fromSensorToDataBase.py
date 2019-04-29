import os
import re
import json
import obd
import pyrebase
import requests
import time

# source = "C:\\Users\\MichaelTelahun\\Documents\\CECS 525\\FinalProject\\OBD2Database\\"
headers = ["RPM", "CoolantTemp", "ThrottlePosition", "EngineLoad", "SpeedKPH", "SpeedMPH", "FuelPressure", "AirIntake", "Degree"]
dataRead = {"RPM" : "", "CoolantTemp" : "", "ThrottlePosition" : "", "EngineLoad" : "", "SpeedKPH" : "", "SpeedMPH" : "", "FuelPressure" : "", "AirIntake" : "", "Degree": ""}
gaugeIndex = 0
toJson = {}
# firebase config and authentication
config = {
    'apiKey': 'AIzaSyCJV79IhlSdhtAOBLJz9H5dAGxfzjSau4Y',
    'authDomain': 'webobdbase.firebaseapp.com',
    'databaseURL': 'https://webobdbase.firebaseio.com',
    'projectId': 'webobdbase',
    'storageBucket': 'webobdbase.appspot.com',
    'messagingSenderId': '184771792235'
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = 'mockemailman@gmail.com'
password = 'JASVT1#PD?3@'
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
# firebase config and authentication



obdSensorData = []
#obd.logger.setLevel(obd.logging.DEBUG)

#connection = obd.Async("COM24")            #same as obd.OBD()
# connection = obd.Async(fast=False)      # the pi cant do fast
connection = obd.Async()


#a callback that prints every new value to console
def new_rpm(r):
    print("RPM:" + str(r.value))
    # obdSensorData.append("RPM: " + str(r.value))
    dataRead["RPM"] = str(r.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1


def coolantTemp(t):
    print("Coolant Temp: " + str(t.value))      #degrees f
    # obdSensorData.append("Coolant Temp: " + str(t.value.to("fahrenheit")))
    dataRead["CoolantTemp"] = str(t.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def throttle(g):
    print("Throttle Position: " + str(g.value))      #percent
    # obdSensorData.append("Throttle Position: " + str(g.value))
    dataRead["ThrottlePosition"] = str(g.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def load(r):
    print("Engine Load:" + str(r.value))
    # obdSensorData.append("Engine Load: " + str(r.value))
    dataRead["EngineLoad"] = str(r.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def speed(r):
    print("Speed Kph:" + str(r.value))              #in km/s
    # print("Speed Mph:", r.value.to("mph"))    #untested, should work
    # obdSensorData.append("Speed Kph: " + str(r.value))
    # obdSensorData.append("Speed Mph: " + str(r.value.to("mph")))
    dataRead["SpeedKPH"] = str(r.value)
    dataRead["SpeedMPH"] = str(r.value.to("mph"))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 2


def fuelPressure(r):
    print("Fuel Pressure kPa:" + str(r.value))              # in kPa
    # obdSensorData.append("Fuel Pressure kPa: " + str(r.value))
    dataRead["FuelPressure"] = str(r.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def intakeTemp(r):
    print("Air Intake Temp:" + str(r.value))
    # obdSensorData.append("Air Intake Temp: " + str(r.value.to("fahrenheit")))
    dataRead["AirIntake"] = str(r.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def racecar(r):
    print("degrees racecar:" + str(r.value))
    # print("**************")
    # obdSensorData.append("degrees racecar: " + str(r.value))
    # obdSensorData.append("**************")
    dataRead["Degree"] = str(r.value)
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1


connection.watch(obd.commands.RPM, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemp)
connection.watch(obd.commands.THROTTLE_POS, callback=throttle)
connection.watch(obd.commands.ENGINE_LOAD, callback=load)
connection.watch(obd.commands.SPEED, callback=speed)
connection.watch(obd.commands.FUEL_PRESSURE, callback=fuelPressure)
connection.watch(obd.commands.INTAKE_TEMP, callback=intakeTemp)
connection.watch(obd.commands.TIMING_ADVANCE, callback=racecar)


#callback will now be fired upon receipt of new values

#   CHANGE THIS TO THE LIVE DATA
# sensorData = open(source + "SensorRead2.txt")
#sensorData = obdSensorData
# object to load
obdDatabase = open('obdData.json', 'w')
obdDatabase.write('[\n')
    
head = True
index = 0

connection.start()

while(1):
    if gaugeIndex >= 9:
        connection.stop()
    connection.stop()

    # data = json.dumps(dataRead)
    # data = "[" + data + "]"
    
    json.dump(dataRead, obdDatabase)
    obdDatabase.write('\n]')
    obdDatabase.close()       
    with open ("obdData.json",'r') as dataToWrite:
        data=json.load(dataToWrite)
    db.child('').remove()
    results = db.child('').set(data, user['idToken'])
    print('\n\\o/')
    obdDatabase = open('obdData.json', 'w')
    obdDatabase.write('[\n')
    gaugeIndex = 0
    dataRead = {"RPM" : "", "CoolantTemp" : "", "ThrottlePosition" : "", "EngineLoad" : "", "SpeedKPH" : "", "SpeedMPH" : "", "FuelPressure" : "", "AirIntake" : "", "Degree": ""}
    connection.start()


# while(1):
#     if len(obdSensorData) == len(headers) + 1: # plus **************
#         connection.stop()

#         for item in obdSensorData:
#             # write to firebase prepare for next object
#             if index == len(headers):
#                 json.dump(toJson, obdDatabase)
#                 obdDatabase.write('\n]')
#                 obdDatabase.close()
#                 with open ("obdData.json",'r') as dataToWrite:
#                     data=json.load(dataToWrite)
#                 db.child('').remove()
#                 results = db.child('').set(data, user['idToken'])
#                 print('\n\\o/')
                
#                 # break # remove this
#                 obdDatabase = open('obdData.json', 'w')
#                 toJson = {}
#                 obdSensorData = []
#                 obdDatabase.write('[\n')
#                 index = 0
#                 connection.start()
#             # last row in set
#             elif index == len(headers) - 1:
#                 item = re.sub('[^0-9.]', '', item)
#                 item = str(round(float(item), 2))
#                 toJson[headers[index]] = item
#                 index = index + 1
#             # all other rows in set
#             else:
#                 celOrFeh = item
#                 item = re.sub('[^0-9.]', '', item)
#                 # always do things in celsius ?
#                 if headers[index] == "CoolantTemp" or headers[index] == "AirIntake" or headers[index] == "OilTemp":
#                     celOrFeh = re.sub('.*:', '', celOrFeh)
#                     celOrFeh = re.sub('[0-9.]', '', celOrFeh).strip()
#                     if celOrFeh == "degF":
#                         item = str((float(item) - 32.0) *(5/9))
#                 item = str(round(float(item), 2))
#                 toJson[headers[index]] = item
#                 index = index + 1
