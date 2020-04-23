import serial
import time
from PyQt5 import QtCore

class RFID():
    ip = None 
    port = None 
    serial = None
    com = None
    connect = False

    VER_COMMAND = [0x02,0xA4]
    READ_COMMAND = b'550D'

    update_count = 0
    update_uid = None

    def __init__(self,ip = None,port = None,com = None):
        self.ip = ip
        self.port = port
        self.com = com
    
    def connect_serial(self):
        self.close()
        if self.com == None:
            addr = self.ip + ":" + str(self.port)
            try:
                self.serial = serial.serial_for_url("socket://" + addr + "/logging=debug")
                self.connect = True
                return True
            except:
                self.serial = None
                self.connect = False
                return False
        else:
            try:
                self.serial = serial.Serial(self.com)
                self.connect = True
                return True
            except:
                self.serial = None
                self.connect = False
                return False

    def get_version(self):
        r = self.write(self.VER_COMMAND)
        return r

    def get_card(self):
        r = self.write(self.READ_COMMAND)
        return r
        

    def write(self,command):
        self.serial.write(command)
        time.sleep(1)
        r = []
        while self.serial.in_waiting:
            r.append(self.serial.read())
        return r

    def close(self):
        if self.serial != None:
            self.serial.close()

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
    rfid = RFID(com=com)
    if rfid.connect_serial():
        print("RFID VERSION:")
        print(rfid.get_version())

        print("RFID READ CARD:")
        print(rfid.get_card()) 

        rfid.close()