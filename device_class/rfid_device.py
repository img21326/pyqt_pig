import serial
import time
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

    name = ""

    def __init__(self, ip=None, port=None, com=None, name=None):
        super().__init__(ip=ip, port=port, com=com)
        self.name = name

    def get_version(self):
        r = self.write(self.VER_COMMAND)
        return r

    def get_card(self):
        r = self.write(self.READ_COMMAND)
        # print(r)
        if (len(r) <= 4):
            self.update_uid = "None"
            # self.update_count = 0
            return False
        else:
            s = ''
            for ch in r:
                ch = ch.decode()
                if ch == '\n' or ord(ch) == 13:
                    continue
                s = s + ch
            # if self.update_uid == s:
            #     self.update_count += 1
            # else:
            #     self.update_count = 0
            self.update_count += 1
            self.update_uid = s

            if (self.update_count >= 4):
                self.close()
            time.sleep(3.5)
            return s

    def listen(self):
        while True:
            try:

                if self.connect_serial() == False:
                    log('error', self.name + ": not connect to rfid device!")
                    print(self.name + ": not connect to rfid device!")
                    time.sleep(3)
                    continue

                self.get_card()
                log('debug', self.name + ": get card code:" + self.update_uid)
                time.sleep(0.3)
            except Exception as e:
                print("RFID READ CARD ERROR:")
                print(str(e))
                log('error',  self.name + " RFID Listen Error:" + str(e))

