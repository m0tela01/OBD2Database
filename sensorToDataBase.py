import os
import re
import json
import pyrebase
import requests

source = "C:\\Users\\MichaelTelahun\\Documents\\CECS 525\\FinalProject\\OBD2Database\\SensorRead.txt"
headers = ["RPM", "CoolantTemp", "ThrottlePosition", "EngineLoad"]

# data sample
# 760.5 revolutions_per_minute
# 90 degC
# 3.9215686274509802 percent
# 28.627450980392158 percent
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
sensorData = open("SensorRead.txt")
#load object
obdData = open('obdData.json', 'w')

head = True
index = 0
obdData.write('[\n')

for item in sensorData:
    # write to firebase prepare for next object
    if index == len(headers):
        obdData.write(']')
        obdData.close()
        with open ("obdData.json",'r') as dataToWrite:
            data=json.load(dataToWrite)
        db.child("").remove()
        results = db.child('').set(data, user['idToken'])
        print('\n( ͡° ͜ʖ ͡°)')
        break # remove this
        obdData = open('obdData.json', 'w')
        obdData.write('[\n')
        index = 0
    # last row in set
    elif index == len(headers) - 1:
        item = re.sub('[^0-9.]', '', item)
        item = str(round(float(item), 3))
        row = headers[index] + ":" + item
        json.dump(row,obdData)
        index = index + 1
        obdData.write('\n')
    # all other rows in set
    else:
        item = re.sub('[^0-9.]', '', item)
        item = str(round(float(item), 3))
        row = headers[index] + ":" + item
        json.dump(row,obdData)
        obdData.write(',\n')
        index = index + 1
        