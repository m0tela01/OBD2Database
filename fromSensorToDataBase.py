import os
import re
import json
import obd
import pyrebase
import requests
import time

source = "C:\\Users\\MichaelTelahun\\Documents\\CECS 525\\FinalProject\\OBD2Database\\"
headers = ["RPM", "CoolantTemp", "ThrottlePosition", "EngineLoad", "SpeedKPH", "SpeedMPH", "AirIntake", "Degree"]
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



obdData = []
#obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.Async("COM24")            #same as obd.OBD()
#connection = obd.OBD("/dev/ttyUSB0")      # ex for linux

#cmd = obd.commands.SPEED
# connection.watch(obd.commands.RPM)  #keep track of RPM
# connection.start()                  #start async update loop
#
# #print(response.value)
# #print(response.value.to("mph"))
# print(connection.query(obd.commands.RPM))   #nonblocking

#a callback that prints every new value to console
def new_rpm(r):
    print("RPM:", r.value)
    time.sleep(2)
    obdData.append(r.value)

def coolantTemp(t):
    print("Coolant Temp:", t.value.to("fahrenheit"))      #degrees f
    obdData.append(t.value.to("fahrenheit"))

def throttle(g):
    print("Throttle Position:", g.value)      #percent
    obdData.append(g.value)

def load(r):
    print("Engine Load:", r.value)
    obdData.append(r.value)

def speed(r):
    print("Speed Kph:", r.value)              #in km/s
    # print("Speed Mph:", r.value.to("mph"))    #untested, should work
    obdData.append(r.value)

def fuelPressure(r):
    print("Fuel Pressure kPa:", r.value)              # in kPa
    obdData.append(r.value)

def intakeTemp(r):
    print("Air Intake Temp:", r.value.to("fahrenheit"))
    obdData.append(r.value.to("fahrenheit"))

def racecar(r):
    print("degrees racecar:", r.value)
    obdData.append(r.value)

def fuel(r):
    print("Fuel Level:", r.value)
    obdData.append(r.value)

def corn(r):
    print("Corn?:", r.value)
    obdData.append(r.value)
    
def oilTemp(r):
    print("oil temp:", r.value.to("fahrenheit"))
    obdData.append(r.value.to("fahrenheit"))
    print("**************")


connection.watch(obd.commands.RPM, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemp)
connection.watch(obd.commands.THROTTLE_POS, callback=throttle)
connection.watch(obd.commands.ENGINE_LOAD, callback=load)
connection.watch(obd.commands.SPEED, callback=speed)
connection.watch(obd.commands.FUEL_PRESSURE, callback=fuelPressure)
connection.watch(obd.commands.INTAKE_TEMP, callback=intakeTemp)
connection.watch(obd.commands.TIMING_ADVANCE, callback=racecar)
connection.watch(obd.commands.FUEL_LEVEL, callback=fuel)
connection.watch(obd.commands.ETHANOL_PERCENT, callback=corn)
connection.watch(obd.commands.OIL_TEMP, callback=oilTemp)
connection.start()

#callback will now be fired upon receipt of new values

time.sleep(60)          #only here to keep program from ending;
# response = connection.query(obd.commands.O2_SENSORS)
# result = response.value
# print(result)
connection.stop()



#   CHANGE THIS TO THE LIVE DATA
sensorData = open(source + "SensorRead2.txt")
#sensorData = obdData
# object to load 
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
        print('\n( ͡° ͜ʖ ͡°)')
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
        