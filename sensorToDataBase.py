import os
import re
import json
import pyrebase
import requests
import time

source = "C:\\Users\\MichaelTelahun\\Documents\\CECS 525\\FinalProject\\OBD2Database\\"
headers = ["RPM", "CoolantTemp", "ThrottlePosition", "EngineLoad", "SpeedKPH", "SpeedMPH", "AirIntake", "Degree"]
toJson = {}

# data sample
# RPM: 768.0 revolutions_per_minute
# Coolant Temp: 221.00000039999995 degF
# Throttle Position: 0.7843137254901961 percent
# Engine Load: 27.058823529411764 percent
# Speed Kph: 0 kph
# Speed Mph: 0.0 mph
# Air Intake Temp: 165.20000039999996 degF
# degrees racecar: 0.0 degree
# **************
# data sample

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

#   CHANGE THIS TO THE LIVE DATA
sensorData = open(source + "SensorRead2.txt")
#load object
obdData = open('obdData.json', 'w')

head = True
index = 0
obdData.write('[\n')

for item in sensorData:
    # write to firebase prepare for next object
    if index == len(headers):
        json.dump(toJson,obdData)
        obdData.write('\n]')
        obdData.close()
        with open ("obdData.json",'r') as dataToWrite:
            data=json.load(dataToWrite)
        db.child("").remove()
        results = db.child('').set(data, user['idToken'])
        print('\n\\o/')
        # break # remove this
        obdData = open('obdData.json', 'w')
        time.sleep(.5)
        toJson = {}
        obdData.write('[\n')
        index = 0
    # last row in set
    elif index == len(headers) - 1:
        item = re.sub('[^0-9.]', '', item)
        item = str(round(float(item), 2))
        toJson[headers[index]] = item
        index = index + 1
    # all other rows in set
    else:
        celOrFeh = item
        item = re.sub('[^0-9.]', '', item)
        # always do things in celsius ?
        if headers[index] == "CoolantTemp" or headers[index] == "AirIntake":
            celOrFeh = re.sub('.*:', '', celOrFeh)
            celOrFeh = re.sub('[0-9.]', '', celOrFeh).strip()
            if celOrFeh == "degF":
                item = str((float(item) - 32.0) *(5/9))
        item = str(round(float(item), 2))
        toJson[headers[index]] = item
        index = index + 1
        