import re
import json
import obd
import pyrebase
import requests


dataRead = {"RPM" : "", "CoolantTemp" : "", "ThrottlePosition" : "", "EngineLoad" : "", "SpeedKPH" : "", "SpeedMPH" : "", "FuelPressure" : "", "AirIntake" : "", "Degree": ""}
gaugeIndex = 0

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

#connection = obd.Async("COM24")            #same as obd.OBD() - windows
# connection = obd.Async(fast=False)      # if the pi cant do fast
connection = obd.Async()


# cleans each value from the sensor
def clean(item):
    item = re.sub('[^0-9.]', '', item)
    item = str(round(float(item), 2))
    return item


#a callback that prints every new value to console
def new_rpm(r):
    print("RPM:" + str(r.value))
    dataRead["RPM"] = clean(str(r.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1


def coolantTemp(t):
    print("Coolant Temp: " + str(t.value))
    dataRead["CoolantTemp"] = clean(str(t.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def throttle(g):
    print("Throttle Position: " + str(g.value))      #percent
    dataRead["ThrottlePosition"] = clean(str(g.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def load(r):
    print("Engine Load:" + str(r.value))
    dataRead["EngineLoad"] = clean(str(r.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def speed(r):
    print("Speed Kph:" + str(r.value))              #in km/s
    dataRead["SpeedKPH"] = clean(str(r.value))
    dataRead["SpeedMPH"] = clean(str(r.value.to("mph")))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 2

def fuelPressure(r):
    print("Fuel Pressure kPa:" + str(r.value))              # in kPa
    dataRead["FuelPressure"] = clean(str(r.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def intakeTemp(r):
    print("Air Intake Temp:" + str(r.value))
    dataRead["AirIntake"] = clean(str(r.value))
    global gaugeIndex
    gaugeIndex = gaugeIndex + 1

def racecar(r):
    print("degrees racecar:" + str(r.value))
    dataRead["Degree"] = clean(str(r.value))
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


#      TEST WITH FILE
# sensorData = open(source + "SensorRead2.txt")

obdDatabase = open('obdData.json', 'w')
obdDatabase.write('[\n')
connection.start()

while(1):
    # when we have a enough data to load to firebase stop
    if gaugeIndex >= 9:
        connection.stop()
    connection.stop()   # insurance
    try:
        json.dump(dataRead, obdDatabase)    # json.dumps gives a string which firebase didnt enjoy
        obdDatabase.write('\n]')
        obdDatabase.close()       

        # since we dont use dumps we have to write then read back from a file :(
        with open ("obdData.json",'r') as dataToWrite:
            data=json.load(dataToWrite)
        db.child('').remove()
        results = db.child('').set(data, user['idToken'])
        print('\n\\o/') # it worked
        obdDatabase = open('obdData.json', 'w')
        # reset everythin for next read
        obdDatabase.write('[\n')
        gaugeIndex = 0
        dataRead = {"RPM" : "", "CoolantTemp" : "", "ThrottlePosition" : "", "EngineLoad" : "", "SpeedKPH" : "", "SpeedMPH" : "", "FuelPressure" : "", "AirIntake" : "", "Degree": ""}
        connection.start()
    except:
        print("O_o") # it didnt work