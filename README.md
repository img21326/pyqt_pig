![screenshot](https://raw.githubusercontent.com/img21326/pyqt_pig/master/screenshot.png)

## Requirements

 - Python3
 - GUI x64 System
 - certifi==2020.4.5.1 
 - PyQt5==5.14.2 
 - PyQt5-sip==12.7.2 
 - pyserial==3.4

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
API_URL = (backend api url)
LOG_FILE = log.txt
LOG_LEVEL = debug|info (choose one)
WEIGHT_PORT = 
WEIGHT_IP = 
WEIGHT_COM = 
RFID_IP = 
RFID_PORT = 
RFID_COM = 
```

 - 如果是透過TCP/IP則輸入PORT與IP
 - 如是透過USB請輸入COM
 - 請勿兩者皆輸入

##  RUN

```
$ python3 main.py
```

##  Features

 - [ ] API Connection
 - [ ] RFID Reader sometime can't scan the card
 - [ ] Complete process
 - [x] Weight Device data lag
 - [x] Add Log
