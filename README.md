## Food Thread
![screenshot](https://github.com/img21326/pyqt_pig/blob/master/screenshot/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202020-06-10%20%E4%B8%8B%E5%8D%884.30.41.png?raw=true)

## Water Thread
![screenshot](https://github.com/img21326/pyqt_pig/blob/master/screenshot/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202020-06-10%20%E4%B8%8B%E5%8D%884.31.00.png?raw=true)

## TCP Connect(水量儀485)
![screenshot](https://github.com/img21326/pyqt_pig/blob/master/screenshot/tcp-sockect-serial.png?raw=true)

## RPI CONNECT TUTORIAL
![screenshot](https://github.com/img21326/pyqt_pig/blob/master/screenshot/rpi-connect.png?raw=true)

## Requirements

 - Python3
 - autopep8==1.5.3
 - click==7.1.2
 - minimalmodbus==1.0.2
 - prompt-toolkit==3.0.5
 - pycodestyle==2.6.0
 - pyserial==3.4
 - six==1.11.0
 - toml==0.10.1
 - tqdm==4.46.0
 - wcwidth==0.1.9

## Install

```
$ git clone https://github.com/img21326/pyqt_pig.git
```

```
$ cd pyqt_pig
```

```
$ pip install -r requirements.txt
```

```
$ cp config.env.example config.env
```

### setup config file

```
$ vim config.env
```

```
[CONFIG]

API_URL =

LOG_FILE = log.txt

LOG_LEVEL = debug|info

[FOOD]

WEIGHT_PORT =

WEIGHT_IP =

WEIGHT_COM =

RFID_IP =

RFID_PORT =

RFID_COM =

[WATER]

RFID_IP =

RFID_PORT =

RFID_COM =

WATER_IP =

WATER_PORT =

WATER_COM =
```

 - 如果是透過TCP/IP則輸入PORT與IP
 - 如是透過USB請輸入COM
 - 請勿兩者皆輸入

##  RUN

```
$ python3 main.py
```

##  RUN WITH DOCKER

### setup docker-compose.yml (連結usb設備)

```
devices:
- /dev/ttyACM0:/dev/ttyACM0 # RFID
- /dev/ttyUSB0:/dev/ttyUSB0 # SERIAL ex:water device
```

### start up

```
docker-compose up -d
```