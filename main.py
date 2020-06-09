from config import Config
from device_class.rfid_device import RFID
from device_class.water_device import Water
from device_class.weight_device import Weight_Device
from logs.logger import log
import threading
import time
import datetime as dt
import os


class PigData():
    in_time = None
    out_time = None
    val = None
    tag_id = None
    _type = None


class Main():
    food_rfid = None
    food_device = None
    food_rfid_thread = None
    food_device_thread = None
    food_main_thread = None

    water_rfid = None
    water_device = None
    water_rfid_thread = None
    water_main_thread = None

    config = None

    def __init__(self):
        self.config = Config.get_instance()

        mode = os.getenv('MODE')

        print("Start with mode:" + str(mode))

        if mode == 'FOOD':
            self.food_rfid = RFID(
                ip=self.config.FOOD_RFID_IP, port=self.config.FOOD_RFID_PORT, com=self.config.FOOD_RFID_COM, name="FOOD_RFID")
            self.food_device = Weight_Device(
                ip=self.config.WEIGHT_IP, port=self.config.WEIGHT_PORT, com=self.config.WEIGHT_COM)
            self.start_food_threads()
            
        if mode == 'WATER':
            self.water_rfid = RFID(
                ip=self.config.WATER_RFID_IP, port=self.config.WATER_RFID_PORT, com=self.config.WATER_RFID_COM, name="WARTER_RFID")
            self.water_device = Water(
                ip=self.config.WATER_IP, port=self.config.WATER_PORT, com=self.config.WATER_COM)
            self.start_water_threads()

        # self.checkDevice()


    def checkDevice(self):
        if (self.food_rfid.connect_serial() and self.food_device.connect_serial() and self.water_rfid.connect_serial() and self.water_device.connect_serial()):
            self.food_rfid.close()
            self.food_device.close()
            self.water_rfid.close()
            self.water_device.close()
        else:
            log('error', "can't connect device with serials!")
            print("Connect Device Error!")

    def start_food_threads(self):
        self.food_rfid_thread = threading.Thread(target=self.food_rfid_listen)
        self.food_rfid_thread.start()

        self.food_device_thread = threading.Thread(
            target=self.food_device_listen)
        self.food_device_thread.start()

        self.food_main_thread = threading.Thread(target=self.food_main_listen)
        self.food_main_thread.start()

    def food_main_listen(self):

        food_pig_data = None

        while True:
            if ((self.food_rfid.update_uid != "None" and self.food_rfid.update_uid != None and len(self.food_rfid.update_uid) > 0) and food_pig_data == None):  # 刷入
                print(len(self.food_rfid.update_uid))
                food_pig_data = PigData()
                food_pig_data.in_time = dt.datetime.now().strftime("%H:%M:%S")
                food_pig_data.tag_id = self.food_rfid.update_uid
                food_pig_data._type = "food"

                logstr = "[FOOD] - get inside - pig uid:" + \
                    str(food_pig_data.tag_id)
                log('info', logstr)
                print(logstr)

                waittime = 0
                while True:
                    if (waittime > 3):
                        food_pig_data = None
                        logstr = "[FOOD] wait for adding food TIMEOUT for 5 sec, delete this record"
                        log('info', logstr)
                        print(logstr)
                        break

                    if (self.food_device.device_val > 0.5):  # 0.5kg
                        break
                    else:
                        waittime += 1

                        logstr = "[FOOD] wait for adding food to 500g, now just:" + \
                            str(self.food_device.device_val / 1000) + "g"
                        log('info', logstr)
                        print(logstr)
                        time.sleep(2.5)
                time.sleep(3)

            change_pig = False
            if (food_pig_data != None):
                if (food_pig_data.tag_id != self.food_rfid.update_uid):
                    change_pig = True

            if ((self.food_rfid.update_uid == "None" or change_pig) and food_pig_data != None):  # 刷出
                food_pig_data.out_time = dt.datetime.now().strftime("%H:%M:%S")
                food_pig_data.val = str(0.5 - self.food_device.device_val)

                logstr = "[FOOD] - get outside - uid:" + \
                    str(food_pig_data.tag_id) + ", eat value: " + str(food_pig_data.val)
                log('info', logstr)
                print(logstr)

                food_pig_data = None
            time.sleep(0.5)

    def food_rfid_listen(self):
        try:
            self.food_rfid.listen()
        except Exception as e:
            print("FOOD RFID ERROR:")
            print(e)
            log('error', "FOOD RFID Listen Error:" + str(e))
            pass

    def food_device_listen(self):
        try:
            self.food_device.listen()
        except Exception as e:
            print("FOOD DEVICE ERROR:")
            print(e)
            log('error', "Food Device Listen Error:" + str(e))
            pass

    def start_water_threads(self):
        self.water_rfid_thread = threading.Thread(target=self.water_rfid_listen)
        self.water_rfid_thread.start()

        self.water_main_thread = threading.Thread(target=self.water_main_listen)
        self.water_main_thread.start()

    def water_main_listen(self):

        water_pig_data = None
        water_val_last = 0

        while True:
            if ((self.water_rfid.update_uid != "None" and self.water_rfid.update_uid != None) and water_pig_data == None):  # 刷入
                water_pig_data = PigData()
                water_pig_data.in_time = dt.datetime.now().strftime("%H:%M:%S")
                water_pig_data.tag_id = self.water_rfid.update_uid
                water_pig_data._type = "water"

                water_val_last = self.water_device.get_value()

                logstr = "[WATER] - get inside - pig uid:" + \
                    str(water_pig_data.tag_id) + ", water val:"  + str(water_val_last)
                log('info', logstr)
                print(logstr)
                time.sleep(3)

            water_change_pig = False
            if (water_pig_data != None):
                if (water_pig_data.tag_id != self.water_rfid.update_uid):
                    water_change_pig = True

            if ((self.water_rfid.update_uid == "None" or water_change_pig) and water_pig_data != None):  # 刷出
                water_pig_data.out_time = dt.datetime.now().strftime("%H:%M:%S")
                water_pig_data.val = self.water_device.get_value() - water_val_last

                logstr = "[WATER] - get outsid - pig uid:" + \
                    str(water_pig_data.tag_id) + ", drink value: " + str(water_pig_data.val)
                log('info', logstr)
                print(logstr)

                water_pig_data = None
            time.sleep(0.5)

    def water_rfid_listen(self):
        try:
            self.water_rfid.listen()
        except Exception as e:
            print("WATER RFID ERROR:")
            print(e)
            log('error', "WATER RFID Listen Error:" + str(e))
            pass 


if __name__ == '__main__':
    main = Main()
