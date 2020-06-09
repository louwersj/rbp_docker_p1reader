
'''
 NAME:
  p1reader.py

  DESC:
  Code is intended to read smart-meter P1 datagram based data and publish the individual data
  using MQTT. Intended use is to "feed" Home Assistant with MQTT based data-points retrieved
  from the smart-meter.
  
  Documentation on P1 standards can be located at the following location;
  https://github.com/louwersj/rbp_docker_p1reader/blob/master/docs/P1_Companion_Standard%20.pdf

  Based upon the original work done by GJ adn forked by JL (Johan Louwers).

  LOG:
  VERSION---DATE--------NAME-------------COMMENT
  0.1       10-2012     GJ               gratis te kopieren en te plakken
  0.2       12-2016     GJ               Database versie
  0.3       11-2017     GJ               EMSR 5.0
  0.4       06-2021     JL               forked from GJ, removed DB version and implemented MQTT
  0.5       06-2021     JL               Full code refactor and prepared it for Docker

  LICENSE:
  Copyright (C) 2014  Johan Louwers

  This code is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This code is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this code; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
  02110-1301, USA.
'''

__author__ = "Johan Louwers"
__copyright__ = "Copyright 2020, Johan Louwers"
__license__ = "GNU GPL v2"
__email__ = "louwersj@gmail.com"

versie = "0.5"
import sys
import serial
import time
import paho.mqtt.publish as publish
from datetime import datetime

################
#Error display #
################
def show_error():
    ft = sys.exc_info()[0]
    fv = sys.exc_info()[1]
    print("Error type: %s" % ft )
    print("Error value: %s" % fv )
    return




def printTerminalLog(logText, logValue):
    print "P1 LOG - ", (datetime.now()), "-", logText, "-", logValue



def p1Communicator():
    '''

    :return:
    '''
    printTerminalLog("reading P1 smartmeter", "start")


#Set MQTT server settings:
    mqttBroker="rbp0.internal.terminalcult.org"
    mqttPort=1883

    printTerminalLog("set MQTT broker server", mqttBroker)
    printTerminalLog("set MQTT broker port", mqttPort)

#Set COM port config
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.bytesize=serial.EIGHTBITS
    ser.parity=serial.PARITY_NONE
    ser.stopbits=serial.STOPBITS_ONE
    ser.xonxoff=0
    ser.rtscts=0
    ser.timeout=20
    ser.port="/dev/ttyUSB0"

#Open COM port
    try:
        ser.open()
        printTerminalLog("opening communication port",ser.name)
    except:
        sys.exit ("Error: could not create connection to com. port %s ."  % ser.name)
        printTerminalLog("opening communication port", "failed")



#Initialize variables and pre-populate them with 0
    p1LineCounter=0           # count lines in P1 message
    datagramLine=0            # count lines in datagram
    datagram=[]               # datagram
    consumedTariff1 = 0       # consumed electricity tariff 1 (total)
    consumedTariff2 = 0       # consumed electricity tariff 2 (total)
    producedTariff1 = 0       # produced electricity tariff 1 (total)
    producedTariff2 = 0       # produced electricity tariff 1 (total)
    consumedTotal=0           # consumed electricity (total)
    producedTotal=0           # produced electricity (total)
    currentTariff = 0         # current tarrif
    gas = 0                   # consumed gas (total)
    electricityConsumed = 0   # consumed electricity (current)
    electricityProduced = 0   # produced electricity (current)
    electricityFlow=0         # current electricity flow (negative numbers is production)
    electricityFlowTarrif1=0         # current electricity flow tarrif 1(negative numbers is production)
    electricityFlowTarrif2=0         # current electricity flow tarrif 1(negative numbers is production)





    while p1LineCounter < 26:
        try:
            p1LineRaw = ser.readline()
        except:
            sys.exit ("Error: unable to read from com. port connection %s ." % ser.name )
            printTerminalLog("Error: unable to read from com. port connection", ser.name)
        datagram.append((str(p1LineRaw)).strip())
        # print all P1 readings to the terminal using the printTerminalLog function.
        printTerminalLog("p1 read RAW", (str(p1LineRaw)).strip())
        p1LineCounter = p1LineCounter +1


# Close port and show status
    try:
        ser.close()
        printTerminalLog("closing communication port","done")
    except:
        sys.exit ("Error closing com.port  %s connection." % ser.name )
        printTerminalLog("closing communication port", "failed")

# Based upon the original code construct of GJ to loop a number of times trough the datagram we read it per datagramLine
# and extract the individual values and populate the associated values. 
# TODO optimize the below construct to prevent the need to loop multiple times. this slows down execution.
    while datagramLine < 26:
        if datagram[datagramLine][0:9] == "1-0:1.8.1":
            consumedTariff1 = int(datagram[datagramLine][10:16])
            printTerminalLog("total consumed electricity tariff 1 in kWh", consumedTariff1)
            consumedTotal = consumedTotal +  int(float(datagram[datagramLine][10:16]))
        elif datagram[datagramLine][0:9] == "1-0:1.8.2":
            consumedTariff2 = int(datagram[datagramLine][10:16])
            printTerminalLog("total consumed electricity tariff 2 in kWh", consumedTariff2)
            consumedTotal = consumedTotal + int(float(datagram[datagramLine][10:16]))
        elif datagram[datagramLine][0:9] == "1-0:2.8.1":
            producedTariff1 = int(datagram[datagramLine][10:16])
            printTerminalLog("total produced electricity tariff 1 kWh", producedTariff1)
            producedTotal = producedTotal + int(float(datagram[datagramLine][10:16]))
        elif datagram[datagramLine][0:9] == "1-0:2.8.2":
            producedTariff2 = int(datagram[datagramLine][10:16])
            printTerminalLog("total produced electricity tariff 2 kWh", producedTariff2)
            producedTotal = producedTotal + int(float(datagram[datagramLine][10:16]))
        elif datagram[datagramLine][0:9] == "1-0:1.7.0":
            electricityConsumed = int(float(datagram[datagramLine][10:16])*1000)
            printTerminalLog("current consumed electricity Watt", electricityConsumed)
        elif datagram[datagramLine][0:9] == "1-0:2.7.0":
            electricityProduced = int(float(datagram[datagramLine][10:16])*1000)
            printTerminalLog("current produced electricity Watt", electricityProduced)
        elif datagram[datagramLine][0:9] == "0-0:96.14":
            currentTariff = int(datagram[datagramLine][12:16])
            printTerminalLog("current tariff", currentTariff)
        elif datagram[datagramLine][0:10] == "0-1:24.2.1":
            gas = int(float(datagram[datagramLine][26:35])*1000)
            if gas != 0:
                printTerminalLog("total consumed gas (Dm3)", gas)
        else:
            pass
        datagramLine = datagramLine +1

# based upon the value of the current tariff (currentTariff) we can determine if we need to use __xx___Tariff1Current or 
# we need to use __xx___Tariff2Current. In every case we want to publish consume and produce values for both tariff 1 as
# well as tariff 2. In case of a certain tariff is active the other will always be 0.
    if currentTariff == 1:
        consumedTariff1Current = electricityConsumed
        consumedTariff2Current = 0
        producedTariff1Current = electricityProduced
        producedTariff2Current = 0
    elif currentTariff == 2:
        consumedTariff1Current = 0
        consumedTariff2Current = electricityConsumed
        producedTariff1Current = 0
        producedTariff2Current = electricityProduced
    else:
        consumedTariff1Current = 0
        consumedTariff2Current = 0
        producedTariff1Current = 0
        producedTariff2Current = 0

    electricityFlowTarrif1 = consumedTariff1Current - producedTariff1Current
    electricityFlowTarrif2 = consumedTariff2Current - producedTariff2Current
    electricityFlow = electricityConsumed - electricityProduced

# publish towards MQTT all total energy consumption data
    publish.single("smartmeter/energy/consumption/total/tarrif1", consumedTariff1, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/consumption/total/tarrif2", consumedTariff2, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/consumption/total/total", consumedTotal, hostname=mqttBroker, port=mqttPort)

# publish towards MQTT all total energy production data
    publish.single("smartmeter/energy/production/total/tarrif1", producedTariff1, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/production/total/tarrif2", producedTariff2, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/consumption/total/total", consumedTotal, hostname=mqttBroker, port=mqttPort)

#publish towards MQTT all current energy consumption data
    publish.single("smartmeter/energy/consumption/current/tarrif1", consumedTariff1Current, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/consumption/current/tarrif2", consumedTariff2Current, hostname=mqttBroker, port=mqttPort)

# publish towards MQTT all current energy production data
    publish.single("smartmeter/energy/production/current/tarrif1", producedTariff1Current, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/production/current/tarrif2", producedTariff2Current, hostname=mqttBroker, port=mqttPort)

# publish towards MQTT all current energy flow data
    publish.single("smartmeter/energy/flow/current", electricityFlow, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/flow/tarrif1", electricityFlowTarrif1, hostname=mqttBroker, port=mqttPort)
    publish.single("smartmeter/energy/flow/tarrif2", electricityFlowTarrif2, hostname=mqttBroker, port=mqttPort)

# publish towards MQTT all gas consumption data. We only do this when value is not 0 because we do not always have a P1
# value for gas total and we do not want to populate the data warehouse with 0 (missed readings) values.
    if gas != 0:
        publish.single("smartmeter/gas/consumption/total", gas, hostname=mqttBroker, port=mqttPort)

    printTerminalLog("reading P1 smartmeter", "stop")
    printTerminalLog("----------------------------------------", "----------------------------------------")



################################################################################################################################################
#Main program
################################################################################################################################################
print ("ESMR 5.0 P1 uitlezer",  versie)
print ("Gemiddelde telegram uitlezen duurt 10 seconden")
print ("Control-C om te stoppen")

sleeptimer = 61
while True:
    time.sleep(sleeptimer)
    p1Communicator()
    printTerminalLog("Schedule reading P1 smartmeter in (seconds)", sleeptimer)
