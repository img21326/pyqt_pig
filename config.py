import configparser
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

            self.WATER_RFID_IP = config['WATER']['RFID_IP']
            self.WATER_RFID_PORT = config['WATER']['RFID_PORT']
            self.WATER_RFID_COM = config['WATER']['RFID_COM']
            self.WATER_IP = config['WATER']['WATER_IP'] 
            self.WATER_PORT = config['WATER']['WATER_PORT']
            self.WATER_COM = config['WATER']['WATER_COM']

            log('debug', 'start config success')

        except:
            log('error', 'please init your env file')
            print("please init your env file")                     
            pass

    @staticmethod
    def get_instance():
        return Config()