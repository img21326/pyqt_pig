import time
import serial
import datetime as dt
from PyQt5 import QtCore
from logs.logger import log
try:
    from device_class.device import Device
except:
    from device import Device


class Weight_Device(Device):
    device_date = None
    device_val = 0

    def listen(self):
        connect_count = 0
        while True:
            if (self.connect_serial() == False):
                log('error', "not connect to weight device!")
                print("not connect to weight device!")
                time.sleep(3)
                continue
            if not self.serial.in_waiting:
                continue
            try:
                v = self.serial.readline().decode()
            except serial.SerialException:
                log('error', "weight device : SerialException!")
                self.close()

            try:
                date_str = v.split('\r')[0]
                date_str = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                self.device_date = date_str.strftime("%H:%M:%S")
                log('debug', "weight device date : " + (self.device_date))
                # print("date:" + self.device_date)
            except Exception as err:
                pass

            try:
                if ('kg' in v):
                    if ('-' in v):
                        v = v.split('-')[1]
                    kg = int(v.split(' ')[4].replace(
                        '.', '').replace('kg\r\n', ''))
                    self.device_val = kg
                    # if (kg != 0):
                    #    print(kg)
                    log('debug', "weight device val : " + str(self.device_val))
            except Exception as e:
                log('error', "weight val error:" + str(e))
                pass
            
            

            # 防止數據堵塞
            if self.device_val == 0:
                connect_count += 1
            if (connect_count > 120):
                connect_count = 0
                self.close()
                log('debug', "weight device : reconnect" )
                time.sleep(0.5)

## not used class
class Weight_Thread(QtCore.QThread):
    update_date = QtCore.pyqtSignal(str)
    update_val = QtCore.pyqtSignal(int)
    weight_device = None

    def __init__(self, device):
        QtCore.QThread.__init__(self)
        self.weight_device = device

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            if self.weight_device.connect_serial() == False:
                print("not connect to weight device!")
                time.sleep(3)
                continue
            try:
                v = self.weight_device.serial.readline().decode()
            except serial.SerialException:
                self.weight_device.close()

            try:
                date_str = v.split('\r')[0]
                date_str = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                self.weight_device.device_date = date_str.strftime("%H:%M:%S")
                # print("date:" + self.device_date)
            except Exception as err:
                pass

            try:
                if ('kg' in v):
                    if ('-' in v):
                        v = v.split('-')[1]
                    kg = int(v.split(' ')[4].replace(
                        '.', '').replace('kg\r\n', ''))
                    self.weight_device.device_val = kg
                    # if (kg != 0):
                    #    print(kg)
            except:
                pass
            self.update_date.emit(self.weight_device.device_date)
            self.update_val.emit(self.weight_device.device_val)
        # self.update.emit(100)
        # for index in range(1, 101):
        #    self.update.emit(index)
        #    time.sleep(0.5)


if __name__ == '__main__':
    # _weight_device = weight_device(
    #     ip = '192.168.1.100',
    #     port = 50000
    # )

    _weight_device = Weight_Device(
        ip='',
        port='',
        com='COM4'
    )

    if (_weight_device.connect_serial()):
        print("ON connect")
        _weight_device.listen()
    else:
        print("Connect Error")

