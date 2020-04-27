import time
import serial

class Device():
    ip = None 
    port = None 
    serial = None
    com = None
    connect = False

    def __init__(self,ip = None,port = None,com = None):
        self.ip = ip
        self.port = port
        self.com = com
    
    def connect_serial(self):
        if (self.ip != '') and (self.port != '') and (self.connect == False):
            addr = self.ip + ":" + str(self.port)
            try:
                self.serial = serial.serial_for_url("socket://" + addr + "/logging=debug")
                self.connect = True
                return True
            except:
                self.close()
                return False
        elif (self.com != '') and (self.connect == False):
            try:
                self.serial = serial.Serial(self.com)
                self.connect = True
                return True
            except Exception as e:
                print(e)
                self.close()
                return False
        elif (self.connect == True):
            return True
        else:
            return False

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
            self.connect = False
            self.serial = None