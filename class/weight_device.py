import serial
import time
import datetime as dt

class weight_device(object):
    ip = '0.0.0.0'
    port = 5000
    serial = None
    com = None
    thread = None
    connect = False

    device_date = None
    device_val = None

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
    
    def listen(self):
        while self.serial != None:
            try:
                v = self.serial.readline().decode()
                #print(v)
            except serial.SerialException:
                self.connect = False
                while self.connect != True:
                    self.connect_serial()
                    time.sleep(3)
            try:
                date_str = v.split('\r')[0]
                date_str = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                self.device_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
                # print("date:" + self.device_date)
            except Exception as err:
                pass

            try:
                if ('kg' in v):
                        kg = int(v.split(' ')[4].replace('.','').replace('kg\r\n',''))
                        self.device_val = kg
                        if (kg != 0):
                            print(kg)
            except:
                pass
            #else:
                #print("not need val:" + v)
                
    def close(self):
        self.serial.close()

            
            


if __name__ == '__main__':
    # _weight_device = weight_device(
    #     ip = '192.168.1.100',
    #     port = 50000
    # )

    _weight_device = weight_device(
        com='COM4'
    )
    
    if (_weight_device.connect_serial()):
        print("ON connect")
        _weight_device.listen()
    else:
        print("Connect Error")


