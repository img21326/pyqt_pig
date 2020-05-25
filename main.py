from PyQt5 import QtWidgets, QtGui, QtCore
from weight_ui import Ui_MainWindow
import sys
import configparser
import time
import threading
import serial
import datetime as dt
from device_class.weight_device import Weight_Device
from device_class.rfid_device import RFID
from logs.logger import log


class Config():
    API_URL = None
    LOG_FILE = None
    LOG_LEVEL = None
    WEIGHT_PORT = None
    WEIGHT_IP = None
    WEIGHT_COM = None
    FOOD_RFID_IP = None
    FOOD_RFID_PORT = None
    FOOD_RFID_COM = None

    logging = None

    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.env')
            self.API_URL = config['CONFIG']['API_URL']
            self.LOG_FILE = config['CONFIG']['LOG_FILE']
            self.LOG_LEVEL = config['CONFIG']['LOG_LEVEL']
            self.WEIGHT_PORT = config['FOOD']['WEIGHT_PORT']
            self.WEIGHT_IP = config['FOOD']['WEIGHT_IP']
            self.WEIGHT_COM = config['FOOD']['WEIGHT_COM']
            self.FOOD_RFID_IP = config['FOOD']['RFID_IP']
            self.FOOD_RFID_PORT = config['FOOD']['RFID_PORT']
            self.FOOD_RFID_COM = config['FOOD']['RFID_COM']

            
            log('debug', 'start config success')

        except:
            log('error', 'please init your env file')
            print("please init your env file")                     
            pass

    @staticmethod
    def get_instance():
        return Config()


class MainWindow(QtWidgets.QMainWindow):
    table_model = []
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model= QtGui.QStandardItemModel(10,4)
        self.model.setHorizontalHeaderLabels(['UID','IN_TIME','OUT_TIME','VAL'])
        self.ui.tableView.setModel(self.model)

        config = Config.get_instance()
        self.weight_device = Weight_Device(
            ip=config.WEIGHT_IP, port=config.WEIGHT_PORT, com=config.WEIGHT_COM)
        self.food_rfid_device = RFID(
            ip=config.FOOD_RFID_IP, port=config.FOOD_RFID_PORT, com=config.FOOD_RFID_COM)

        if (self.weight_device.connect_serial() and self.food_rfid_device.connect_serial()):
            self.weight_device.close()
            self.food_rfid_device.close()
        else:
            log('error', "can't connect device with serials!")
            print("Connect Device Error!")
            

        self.main_work_thread = FoodWorkThread(
            self.weight_device, self.food_rfid_device)
        self.main_work_thread.update_uid.connect(self.rfid_update_uid)
        self.main_work_thread.update_count.connect(self.rfid_update_count)
        self.main_work_thread.update_val.connect(self.weight_update_value)
        self.main_work_thread.update_date.connect(self.weight_update_date)
        self.main_work_thread.update_table.connect(self.update_table)
        self.main_work_thread.start()
        # self.weight_listen_thread = Weight_Thread(self.weight_device)
        # self.weight_listen_thread.update_date.connect(self.weight_update_date)
        # self.weight_listen_thread.update_val.connect(self.weight_update_value)
        # self.weight_listen_thread.start()

    def rfid_update_count(self, data):
        self.ui.label_food_rfid_value_2.setText(str(data))

    def rfid_update_uid(self, data):
        self.ui.label_food_rfid_value.setText(data)

    def weight_update_date(self, data):
        self.ui.label_weight_datetime.setText(data)

    def weight_update_value(self, data):
        self.ui.label_weight_value.setText(str(data))
    
    def update_table(self, obj):
        self.table_model.append(obj)

        if (len(self.table_model) > 10):
            self.table_model.pop(0)

        reversed_arr = self.table_model[::-1]

        for i,obj in enumerate(reversed_arr):
            in_time = QtGui.QStandardItem(obj.in_time)
            out_time = QtGui.QStandardItem(obj.out_time)
            tag_id = QtGui.QStandardItem(obj.tag_id)
            eat_val = QtGui.QStandardItem(obj.eat_val)
            self.model.setItem(i,0,tag_id)
            self.model.setItem(i,1,in_time)
            self.model.setItem(i,2,out_time)
            self.model.setItem(i,3,eat_val)
        self.ui.tableView.setModel(self.model)

class PigData():
    in_time = None
    out_time = None
    eat_val = None
    tag_id = None

class FoodWorkThread(QtCore.QThread):
    # weight
    update_date = QtCore.pyqtSignal(str)
    update_val = QtCore.pyqtSignal(int)

    # rfid
    update_count = QtCore.pyqtSignal(int)
    update_uid = QtCore.pyqtSignal(str)

    # table
    update_table = QtCore.pyqtSignal(object)

    # device
    weight_device = None
    food_rfid_device = None

    # tread
    rfid_thread = None
    weight_thread = None

    def __init__(self, weight_device, food_rfid_device):
        QtCore.QThread.__init__(self)
        self.weight_device = weight_device
        self.food_rfid_device = food_rfid_device

    def __del__(self):
        self.wait()

    def run(self):
        self.rfid_thread = threading.Thread(target=self.run_rfid_thread)
        self.weight_thread = threading.Thread(target=self.run_weight_thread)
        self.rfid_thread.start()
        self.weight_thread.start()

        # rfid_onload = False
        pig_data = None

        while True:
            self.update_uid.emit(self.food_rfid_device.update_uid)
            self.update_count.emit(self.food_rfid_device.update_count)
            # print(self.food_rfid_device.update_uid)

            if ((self.food_rfid_device.update_uid != "None" and self.food_rfid_device.update_uid != None) and pig_data == None): # 刷入
                pig_data = PigData()
                pig_data.in_time = dt.datetime.now().strftime("%H:%M:%S")
                pig_data.tag_id = self.food_rfid_device.update_uid

                log('info', "get inside uid:" + str(pig_data.tag_id))

            change_pig = False
            if (pig_data != None):
                if (pig_data.tag_id != self.food_rfid_device.update_uid):
                    change_pig = True
                
            if ((self.food_rfid_device.update_uid == "None" or change_pig) and pig_data != None): # 刷出
                pig_data.out_time = dt.datetime.now().strftime("%H:%M:%S")
                pig_data.eat_val = str(self.weight_device.device_val)
                self.update_table.emit(pig_data)

                log('info', "get out uid:" + str(pig_data.tag_id) + ", eat value: " + str(pig_data.eat_val))

                pig_data = None

            self.update_date.emit(self.weight_device.device_date)
            self.update_val.emit(self.weight_device.device_val)

            # self.update_table.emit(self.weight_device.device_val)

            time.sleep(1/23)

    def run_rfid_thread(self):
        try:
            self.food_rfid_device.listen()
        except Exception as e:
            log('error', "RFID Listen Error:" + str(e))
            pass

    def run_weight_thread(self):
        try:
            self.weight_device.listen()
        except Exception as e:
            log('error', "Weight Listen Error:" + str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
