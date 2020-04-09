import serial
import time
class RFID():
    ser = None

    VER_COMMAND = [0x02,0xA4]
    READ_COMMAND = b'550D'

    def __init__(self,port = None):
        if port == None:
            port = "/dev/tty.usbmodem201201011"
        
        try:
            self.ser = serial.Serial(port)
            print(self.ser)
        except Exception as e:
            print("connect port error:")
            print(e)
            exit()
    
    def get_version(self):
        r = self.write(self.VER_COMMAND)
        return r

    def get_card(self):
        r = self.write(self.READ_COMMAND)
        return r
        

    def write(self,command):
        self.ser.write(command)
        time.sleep(1)
        r = []
        while self.ser.in_waiting:
            r.append(self.ser.read())
        return r

    def close(self):
        self.ser.close()

    @staticmethod
    def get_instance(port = None):
        rfid = RFID(port)
        return rfid

if __name__ == "__main__":
    import sys
    try:
        port = sys.argv[1]
    except:
        port = None
    rfid = RFID.get_instance(port)
    print("RFID VERSION:")
    print(rfid.get_version())

    print("RFID READ CARD:")
    print(rfid.get_card()) 

    rfid.close()