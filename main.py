from PyQt5 import QtWidgets, QtGui, QtCore
from weight_ui import Ui_MainWindow
import sys
import configparser

class Config():
     API_URL = None
     WEIGHT_PORT = None
     WEIGHT_IP = None
     WEIGHT_COM = None
     RFID_IP = None
     RFID_PORT = None
     RFID_COM = None

     def __init__(self):
          config = configparser.ConfigParser()
          try:
               config.read('config.env')
               self.API_URL = config['CONFIG']['API_URL']
               self.WEIGHT_PORT = config['CONFIG']['WEIGHT_PORT']
               self.WEIGHT_IP = config['CONFIG']['WEIGHT_IP']
               self.WEIGHT_COM = config['CONFIG']['WEIGHT_COM']
               self.RFID_IP = config['CONFIG']['RFID_IP']
               self.RFID_PORT = config['CONFIG']['RFID_PORT']
               self.RFID_COM = config['CONFIG']['RFID_COM']
          except:
               print("please init your env file")
               exit()

     @staticmethod
     def get_instance():
          return Config()

class MainWindow(QtWidgets.QMainWindow):
     def __init__(self):
         super(MainWindow, self).__init__()
         self.ui = Ui_MainWindow()
         self.ui.setupUi(self)


if __name__ == '__main__':
     config = Config.get_instance()

     app = QtWidgets.QApplication([])
     window = MainWindow()
     window.show()
     sys.exit(app.exec_())