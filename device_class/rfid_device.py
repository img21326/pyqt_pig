import serial
import time
from PyQt5 import QtCore
from logs.logger import log
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
        print(r)
        if (len(r) == 4):
            self.update_uid = "None"
            self.update_count = 0
            return False
        else:
            s = ''
            for ch in r:
                ch = ch.decode()
                if ch == '\n' or ord(ch) == 13:
                    continue
                s = s + ch
            if self.update_uid == s:
                self.update_count += 1
            else:
                self.update_count = 0
            self.update_uid = s
            return s

    def listen(self):
        while True:
            if self.connect_serial() == False:
                log('error', "not connect to rfid device!")
                print("not connect to rfid device!")
                time.sleep(3)
                continue

            self.get_card()
            log('debug', "get card code:" + self.update_uid)
            time.sleep(0.05)


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
