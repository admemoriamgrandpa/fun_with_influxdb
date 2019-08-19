import socket
import struct
import utime
import machine

class TIMESERVER:
    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_DELTA = 2208988800 # NTP DELTA i.e from 12 midnight of 01/01/1900 - unix epoch
    host = "pool.ntp.org" #ntp domain name

    def time(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(self.host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        return val - self.NTP_DELTA

    # There's currently no timezone support in MicroPython, so
    # utime.localtime() will return UTC time (as if it was .gmtime())
    def settime(self):
        t = time()
        tm = utime.localtime(t)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)
