import obd
import time
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

def coolantTemp(t):
    print("Coolant Temp:", t.value.to("fahrenheit"))      #degrees f

def throttle(g):
    print("Throttle Position:", g.value)      #percent

def load(r):
    print("Engine Load:", r.value)

def speed(r):
    print("Speed Kph:", r.value)              #in km/s
    print("Speed Mph:", r.value.to("mph"))    #untested, should work

def fuelPressure(r):
    print("Fuel Pressure kPa:", r.value)              # in kPa

def intakeTemp(r):
    print("Air Intake Temp:", r.value.to("fahrenheit"))

def racecar(r):
    print("degrees racecar:", r.value)

def fuel(r):
    print("Fuel Level:", r.value)

def corn(r):
    print("Corn?:", r.value)
    
def oilTemp(r):
    print("oil temp:", r.value.to("fahrenheit"))



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
