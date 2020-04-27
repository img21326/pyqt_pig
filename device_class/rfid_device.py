import serial
import time
from PyQt5 import QtCore

try:
    from device_class.device import Device
except:
    from device import Device

class RFID(Device):

    VER_COMMAND = [0x02,0xA4]
    READ_COMMAND = b'550D'

    update_count = 0
    update_uid = None
    
    def get_version(self):
        r = self.write(self.VER_COMMAND)
        return r

    def get_card(self):
        r = self.write(self.READ_COMMAND)
        return r

class RFID_Thread(QtCore.QThread):
    update_count = QtCore.pyqtSignal(int)
    update_uid = QtCore.pyqtSignal(str)
    rfid_device = None

    def __init__(self, device):
        QtCore.QThread.__init__(self)
        self.rfid_device = device

    def __del__(self):
        self.wait()

    def run(self):
        while self.rfid_device.serial != None:

            self.update_count.emit(self.rfid_device.update_count)
            self.update_uid.emit(self.rfid_device.update_uid)


if __name__ == "__main__":
    import sys
    try:
        com = sys.argv[1]
    except:
        com = None
    rfid = RFID(ip='',port='',com=com)
    if rfid.connect_serial():
        print("RFID VERSION:")
        print(rfid.get_version())

        print("RFID READ CARD:")
        print(rfid.get_card()) 

        rfid.close()