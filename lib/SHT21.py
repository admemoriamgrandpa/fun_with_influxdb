# A dirty class to convert temperature and humidity readings from called SHT21COOKIES
#connect to bluetooth
#Get Value
#Extract Value
#split temperature and humidity

from network import Bluetooth
from ucollections import namedtuple
import ubinascii
import ustruct


class sht21:
    bt = Bluetooth()
    conn = None


    def start_sht21(self):
        self.bt.init()

    @classmethod
    def connect_to_sht21(cls):
        try:
            cls.conn = sht21.bt.connect(b'\xbc\x6a\x29\xc0\xf0\x69') # hard coded ble mac from the device
        except:
            print("Connection refused")

    def extract_value(self):
        reading = namedtuple('reading', 'temperature humidity')
        try:
            x = ubinascii.hexlify(sht21.conn.services()[3].characteristics()[0].read()).decode() # read value and convert to hexadecimals and strings

            #extraction temperature values
            tem = str(ustruct.unpack("i",ubinascii.unhexlify(x[:4] + '0000'))[0])
            tem = tem[:2] + '.' + tem[2:]
            print("The ambient temperature is: " + tem)

            # extract humidity values
            hum = str(ustruct.unpack("i",ubinascii.unhexlify(x[4:] + '0000'))[0])
            hum = hum[:2] + '.' + hum[2:]
            print("The ambient humidity is: " + hum)
            return reading(tem, hum)

        except:
            print("No connection established ...")
