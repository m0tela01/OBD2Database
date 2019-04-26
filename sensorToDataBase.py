import os
import json

source = "C:\\Users\\Michael Telahun\\Documents\\OBD2Database\\SensorRead.txt"

# 760.5 revolutions_per_minute
# 90 degC
# 3.9215686274509802 percent
# 28.627450980392158 percent
# **************


data = ["RPM", "Cool Temp", "Throttle Position", "Engine Load"]

senorData = open("SensorRead.txt")
obdData = open('obdData.json', 'w')

head = True
index = 0

for item in senorData:
    if senorData == "**************":
        obdData.write(']')
        break
        

obdData.write('[\n')
for row in reader:
    if head:
        head = False
        continue
    else:
        if index < count:
            json.dump(row,obdData)
            obdData.write(',\n')
            index = index + 1
        elif index == count:
            json.dump(row,obdData)
            obdData.write('\n')
            index = index + 1
        else:
            break
obdData.write(']')
