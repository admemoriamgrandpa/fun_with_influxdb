# <h6>**Introduction**

This code performs six functions:
* Connect to WLAN
*  Get time from NTP server
*  Connect to SHT21 smart gadget
*  Get Temperature and Humidity Reading from smart gadget
*  Get temperature, humidity and accelerometer readings from Pysense
*  Upload readings to an influxdb server on the same LAN
 

The code can be uploaded to the pysense board through **FTP** amongt other ways. Ensure that the
device is on the same LAN with your computer before uploading the code. Press the reset button on the Pysense board to run.

Use Putty (or any terminal emulator) to see the printouts on the screen.

**TODOS**

Connect two Fipy boards and dynamically change communication technology based on climatic conditions.

Reconfiguring some physical parameters at run time.

 