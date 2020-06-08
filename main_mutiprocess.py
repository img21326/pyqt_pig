from config import Config
from device_class.rfid_device import RFID
from device_class.water_device import Water
from device_class.weight_device import Weight_Device
from logs.logger import log
import threading
import time
import multiprocessing
import datetime as dt

class PigData():
    in_time = None
    out_time = None
    val = None
    tag_id = None
    _type = None

def start_food_thread(food_rfid, food_device):
    def food_rfid_listen():
        try:
            food_rfid.listen()
        except Exception as e:
            print("FOOD RFID ERROR:")
            print(e)
            log('error', "FOOD RFID Listen Error:" + str(e))
            pass

    def food_device_listen():
        try:
            food_device.listen()
        except Exception as e:
            print("FOOD DEVICE ERROR:")
            print(e)
            log('error', "Food Device Listen Error:" + str(e))
            pass

    def food_main_listen():
        food_pig_data = None

        while True:
            if ((food_rfid.update_uid != "None" and food_rfid.update_uid != None) and food_pig_data == None):  # 刷入
                food_pig_data = PigData()
                food_pig_data.in_time = dt.datetime.now().strftime("%H:%M:%S")
                food_pig_data.tag_id = food_rfid.update_uid
                food_pig_data._type = "food"

                logstr = "[FOOD] - get inside - pig uid:" + \
                    str(food_pig_data.tag_id)
                log('info', logstr)
                print(logstr)

                waittime = 0
                while True:
                    if (waittime > 5):
                        food_pig_data = None
                        logstr = "[FOOD] wait for adding food TIMEOUT for 5 sec, delete this record"
                        log('info', logstr)
                        print(logstr)
                        break

                    if (food_device.device_val > 0.5):  # 0.5kg
                        break
                    else:
                        waittime += 1

                        logstr = "[FOOD] wait for adding food to 500g, now just:" + \
                            str(food_device.device_val / 1000) + "g"
                        log('info', logstr)
                        print(logstr)
                        time.sleep(1)

            change_pig = False
            if (food_pig_data != None):
                if (food_pig_data.tag_id != food_rfid.update_uid):
                    change_pig = True

            if ((food_rfid.update_uid == "None" or change_pig) and food_pig_data != None):  # 刷出
                food_pig_data.out_time = dt.datetime.now().strftime("%H:%M:%S")
                food_pig_data.val = str(0.5 - food_device.device_val)

                logstr = "[FOOD] - get outside - uid:" + \
                    str(food_pig_data.tag_id) + ", eat value: " + str(food_pig_data.val)
                log('info', logstr)
                print(logstr)

                food_pig_data = None
            time.sleep(0.001)

    food_rfid_thread = threading.Thread(target=food_rfid_listen)
    food_rfid_thread.start()

    food_device_thread = threading.Thread(target=food_device_listen)
    food_device_thread.start()

    food_main_thread = threading.Thread(target=food_main_listen)
    food_main_thread.start()


def start_water_thread(water_rfid,water_device):
    def water_rfid_listen():
        try:
            water_rfid.listen()
        except Exception as e:
            print("WATER RFID ERROR:")
            print(e)
            log('error', "WATER RFID Listen Error:" + str(e))
            pass 

    def water_main_listen():
        water_pig_data = None
        water_val_last = 0

        while True:
            if ((water_rfid.update_uid != "None" and water_rfid.update_uid != None) and water_pig_data == None):  # 刷入
                water_pig_data = PigData()
                water_pig_data.in_time = dt.datetime.now().strftime("%H:%M:%S")
                water_pig_data.tag_id = water_rfid.update_uid
                water_pig_data._type = "water"

                water_val_last = water_device.get_value()

                logstr = "[WATER] - get inside - pig uid:" + \
                    str(water_pig_data.tag_id) + ", water val:"  + str(water_val_last)
                log('info', logstr)
                print(logstr)

            water_change_pig = False
            if (water_pig_data != None):
                if (water_pig_data.tag_id != water_rfid.update_uid):
                    water_change_pig = True

            if ((water_rfid.update_uid == "None" or water_change_pig) and water_pig_data != None):  # 刷出
                water_pig_data.out_time = dt.datetime.now().strftime("%H:%M:%S")
                water_pig_data.val = water_device.get_value() - water_val_last

                logstr = "[WATER] - get outsid - pig uid:" + \
                    str(water_pig_data.tag_id) + ", drink value: " + str(water_pig_data.val)
                log('info', logstr)
                print(logstr)

                water_pig_data = None
            time.sleep(0.001)

    water_rfid_thread = threading.Thread(target=water_rfid_listen) 
    water_rfid_thread.start()

    water_main_thread = threading.Thread(target=water_main_listen)
    water_main_thread.start()


if __name__ == "__main__":
    config = Config.get_instance()

    food_rfid = RFID(
        ip=config.FOOD_RFID_IP, port=config.FOOD_RFID_PORT, com=config.FOOD_RFID_COM, name="FOOD_RFID")
    food_device = Weight_Device(
        ip=config.WEIGHT_IP, port=config.WEIGHT_PORT, com=config.WEIGHT_COM)

    water_rfid = RFID(
        ip=config.WATER_RFID_IP, port=config.WATER_RFID_PORT, com=config.WATER_RFID_COM, name="WARTER_RFID")
    water_device = Water(
        ip=config.WATER_IP, port=config.WATER_PORT, com=config.WATER_COM)

    if (food_rfid.connect_serial() and food_device.connect_serial() and water_rfid.connect_serial() and water_device.connect_serial()):
        food_rfid.close()
        food_device.close()
        water_rfid.close()
        water_device.close()
    else:
        log('error', "can't connect device with serials!")
        print("Connect Device Error!")

    food_multi = multiprocessing.Process(target=start_food_thread, args=(food_rfid,food_device))
    food_multi.start()

    water_multi = multiprocessing.Process(target=start_water_thread, args=(water_rfid,water_device))
    water_multi.start()

    while True:
        time.sleep(1)