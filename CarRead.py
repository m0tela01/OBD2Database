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
    print(r.value)
    time.sleep(2)

def coolantTemp(t):
    print(t.value)      #degrees science

def throttle(g):
    print(g.value)      #percent

def load(r):
    print(r.value)

def speed(r):
    print(r.value)              #in km/s
    print(r.value.to("mph"))    #untested, should work
    print("**************")


connection.watch(obd.commands.RPM, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemp)
connection.watch(obd.commands.THROTTLE_POS, callback=throttle)
connection.watch(obd.commands.ENGINE_LOAD, callback=load)
connection.watch(obd.commands.SPEED, callback=speed)
connection.start()

#callback will now be fired upon receipt of new values

time.sleep(60)
# response = connection.query(obd.commands.O2_SENSORS)
# result = response.value
# print(result)
connection.stop()
