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
    RFID_IP = None
    RFID_PORT = None
    RFID_COM = None

    logging = None

    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.env')
            self.API_URL = config['CONFIG']['API_URL']
            self.LOG_FILE = config['CONFIG']['LOG_FILE']
            self.LOG_LEVEL = config['CONFIG']['LOG_LEVEL']
            self.WEIGHT_PORT = config['CONFIG']['WEIGHT_PORT']
            self.WEIGHT_IP = config['CONFIG']['WEIGHT_IP']
            self.WEIGHT_COM = config['CONFIG']['WEIGHT_COM']
            self.RFID_IP = config['CONFIG']['RFID_IP']
            self.RFID_PORT = config['CONFIG']['RFID_PORT']
            self.RFID_COM = config['CONFIG']['RFID_COM']

            
            log('debug', 'start config success')

        except:
            log('error', 'please init your env file')
            print("please init your env file")                     
            pass

    @staticmethod
    def get_instance():
        return Config()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        config = Config.get_instance()
        self.weight_device = Weight_Device(
            ip=config.WEIGHT_IP, port=config.WEIGHT_PORT, com=config.WEIGHT_COM)
        self.rfid_device = RFID(
            ip=config.RFID_IP, port=config.RFID_PORT, com=config.RFID_COM)

        if (self.weight_device.connect_serial() and self.rfid_device.connect_serial()):
            self.weight_device.close()
            self.rfid_device.close()
        else:
            log('error', "can't connect device with serials!")
            print("Connect Device Error!")
            

        self.main_work_thread = MianWorkThread(
            self.weight_device, self.rfid_device)
        self.main_work_thread.update_uid.connect(self.rfid_update_uid)
        self.main_work_thread.update_count.connect(self.rfid_update_count)
        self.main_work_thread.update_val.connect(self.weight_update_value)
        self.main_work_thread.update_date.connect(self.weight_update_date)
        self.main_work_thread.start()
        # self.weight_listen_thread = Weight_Thread(self.weight_device)
        # self.weight_listen_thread.update_date.connect(self.weight_update_date)
        # self.weight_listen_thread.update_val.connect(self.weight_update_value)
        # self.weight_listen_thread.start()

    def rfid_update_count(self, data):
        self.ui.label_rfid_value_2.setText(str(data))

    def rfid_update_uid(self, data):
        self.ui.label_rfid_value.setText(data)

    def weight_update_date(self, data):
        self.ui.label_weight_datetime.setText(data)

    def weight_update_value(self, data):
        self.ui.label_weight_value.setText(str(data))


class MianWorkThread(QtCore.QThread):
    # weight
    update_date = QtCore.pyqtSignal(str)
    update_val = QtCore.pyqtSignal(int)

    # rfid
    update_count = QtCore.pyqtSignal(int)
    update_uid = QtCore.pyqtSignal(str)

    # device
    weight_device = None
    rfid_device = None

    # tread
    rfid_thread = None
    weight_thread = None

    def __init__(self, weight_device, rfid_device):
        QtCore.QThread.__init__(self)
        self.weight_device = weight_device
        self.rfid_device = rfid_device

    def __del__(self):
        self.wait()

    def run(self):
        self.rfid_thread = threading.Thread(target=self.run_rfid_thread)
        self.weight_thread = threading.Thread(target=self.run_weight_thread)
        self.rfid_thread.start()
        self.weight_thread.start()
        while True:
            self.update_uid.emit(self.rfid_device.update_uid)
            self.update_count.emit(self.rfid_device.update_count)
            # print(self.rfid_device.update_uid)

            self.update_date.emit(self.weight_device.device_date)
            self.update_val.emit(self.weight_device.device_val)

            time.sleep(1.2)

    def run_rfid_thread(self):
        try:
            self.rfid_device.listen()
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
