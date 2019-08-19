from connect_to_wifi import CONNECT_TO_WIFI
from timeserver import TIMESERVER
from machine import RTC
from network import WLAN
from SHT21 import sht21
import time
import pycom
import ssl
import urequests


pycom.heartbeat(False) # put off the LED

connect_timeout = 6000 # It is actually 5000ms but 1 second more to avoid perpetual loop
rtc = RTC()
sht21_smart_gadget = sht21()
lanw = CONNECT_TO_WIFI()


while not lanw.wlan.isconnected(): # connection must be established before running the main code
    lanw.net_setup()
    now = time.ticks_ms() # Wait for a minimum connection timeout before another iteration.
    while time.ticks_diff(time.ticks_ms(), now) > connect_timeout:
        pass
    if not lanw.wlan.isconnected():
        #red blink to show that wifi is not connected
        #todo put it in a class
        pycom.rgbled(0xFF0000)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0xFF0000)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0xFF0000)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0xFF0000)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)

    else:
        #blink green to show success in connection
        pycom.rgbled(0x00FF00)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0x00FF00)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0x00FF00)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)
        time.sleep_ms(600)
        pycom.rgbled(0x00FF00)
        time.sleep_ms(600)
        pycom.rgbled(0x000000)


rtc.ntp_sync("pool.ntp.org",update_period=900) # connecting to ntp
time.sleep_ms(750) #offset for round trip time to the ntp server.
time.timezone(7200)

#connect to the BLE Device
try:
    sht21_smart_gadget.start_sht21()
    sht21_smart_gadget.connect_to_sht21()

except:
    print("BLE connection failed")
#creating database - is this the best place to put this?
try:
    resp = urequests.post('http://192.168.0.102:8086/query?q=CREATE%20DATABASE%20failoverdb')
    if resp.status_code == 200 or 204:
        print("Database Created ...")
    else:
        print("Database creation unsuccessful")
except:
    print("OS Error")
