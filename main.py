# Author; Stanley C Nwabuona <stanley.nwabuona@pro2future.at>


import time
import utime
import ujson
import socket
import ssl
import struct
import urequests
from machine import Pin
from network import WLAN
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from connect_to_wifi import CONNECT_TO_WIFI
from timeserver import TIMESERVER
from machine import RTC

# Todos
# Stage 2:
# 1. Connection between two fypis
# 2. Switch between networks (Just playing around)
# 2. Switch between networks based on temperature or pressure reading
# Meeting with Konrad for additional features


# connecting to the WLAN
py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

#sensor_values = [{"name" : "temperature", "columns" : ["value", "host", "region", "time"], "points" : []}, {"name" : "humidity", "columns" : ["value", "host", "region", "time"], "points" : []}, {"name" : "accelerometer", "columns" : ["pitch", "roll", "host", "region", "time"], "points" : []}]
sensor_values = {"temperature": "", "humidity": "", "accelerometer": ""}
#startConnection = CONNECT_TO_WIFI().net_setup()

while True:
    if lanw.wlan.isconnected():
        print("Taking Readings from sensors")
        #sensor_values["board_tp"] = mp.temperature()
        #sensor_values["board_hum"] = mp.humidity()
        #sensor_values["acc_roll"] = li.roll()
        #sensor_values["acc_pitch"] = li.pitch()
        #print("MPL3115A2 temperature: " + str(mp.temperature()))
        #print("Altitude: " + str(mp.altitude()))
        #print("Pressure: " + str(mpp.pressure()))
        #print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
        #print("Dew point: "+ str(si.dew_point()) + " deg C")
        #t_ambient = 24.4
        #print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
        #print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
        #print("Acceleration: " + str(li.acceleration()))
        #print("Roll: " + str(li.roll()))
        #print("Pitch: " + str(li.pitch()))
        #print("Battery voltage: " + str(py.read_battery_voltage()))


        if not rtc.synced():
            rtc.ntp_sync("pool.ntp.org",update_period=900) # connecting to ntp __not sure if it will resync from the bootloader
            time.sleep_ms(750) #offset for round trip time to the ntp server.
            utime.timezone(7200)



        try:
            # get ble values;
            ble_val = sht21_smart_gadget.extract_value()
            sensor_values["temperature"] = "temperature,location=office,host=pysense_board " + "value=" + str(mp.temperature()) + " " + str(time.time()) + " \n " + "temperature,location=office,host=sht21_smart_gadget " + "value=" + ble_val.temperature + " " + str(time.time()) + " \n "
            sensor_values["humidity"] = "humidity,location=office,host=board " + "value=" + str(si.humidity()) + " " + str(time.time()) + " \n " + "humidity,location=office,host=sht21_smart_gadget " + "value=" + ble_val.humidity + " " + str(time.time()) + " \n "
            sensor_values["accelerometer"] = "accelerometer,location=office,host=board " + "roll=" + str(li.roll()) + "," + "pitch=" + str(li.pitch()) + " " + str(time.time())


            #send to influx
            print(ble_val.humidity,ble_val.temperature)
            resp = urequests.post('http://192.168.0.102:8086/write?db=failoverdb', data=sensor_values["temperature"]+sensor_values["humidity"]+sensor_values["accelerometer"])
            print(resp.status_code)
            if resp.status_code == 204 or 200:
                pass
            else:
                print(resp.text)

            #sleep for 20 minutes
            time.sleep(1200)
        except:
            print("Ble data could not be fetched")
            #add later  - It could be BLE, WIFI or database.
            # Soultion, if BLE is still connected, do nothing else reconnect
            # Solution, if wifi is still connected, do nothing, else reconnect
            # if it is not any of this solutions, print server is not reachable or learn how to raise try error
            time.sleep(120)
    else:
        #reconnect and sleep for 6 seconds
        CONNECT_TO_WIFI().net_setup()
        time.sleep(6)
