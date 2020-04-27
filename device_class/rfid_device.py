import serial
import time
from PyQt5 import QtCore

try:
    from device_class.device import Device
except:
    from device import Device


class RFID(Device):

    VER_COMMAND = [0x02, 0xA4]
    READ_COMMAND = [0x55, 0x0D]

    update_count = 0
    update_uid = None

    def get_version(self):
        r = self.write(self.VER_COMMAND)
        return r

    def get_card(self):
        r = self.write(self.READ_COMMAND)
        if (len(r) == 4):
            self.update_uid = "None"
            self.update_count = 0
            return False
        else:
            s = ''
            for ch in r:
                ch = ch.decode()
                if ch != '\n':
                    s = s + ch
            self.update_uid = s
            self.update_count += 1
            return s


if __name__ == "__main__":
    import sys
    try:
        com = sys.argv[1]
    except:
        com = None
    rfid = RFID(ip='', port='', com=com)
    if rfid.connect_serial():
        print("RFID VERSION:")
        print(rfid.get_version())

        print("RFID READ CARD:")
        print(rfid.get_card())

        rfid.close()
