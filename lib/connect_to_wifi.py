from network import WLAN
import machine
import time

class CONNECT_TO_WIFI:
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()

    def net_setup(self):
        if not self.wlan.isconnected():
            for net in self.nets:
                if net.ssid == 'Area41':
                    print('Network found!')
                    self.wlan.connect(net.ssid, auth=(net.sec, '39532213'), timeout=5000)
                    while not self.wlan.isconnected():
                        machine.idle()
                    print("WLAN connection succeeded")
                    break
        else:
            print("Connection already established!")
