import serial
import time
class RFID():
    ip = None 
    port = None 
    serial = None
    com = None
    thread = None
    connect = False

    VER_COMMAND = [0x02,0xA4]
    READ_COMMAND = b'550D'

    def __init__(self,ip = None,port = None,com = None):
        self.ip = ip
        self.port = port
        self.com = com
    
    def connect_serial(self):
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
        self.serial.close()


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