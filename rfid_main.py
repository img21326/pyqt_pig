from device_class.rfid_device import RFID

if __name__ == "__main__":
    import sys
    try:
        com = sys.argv[1]
    except:
        com = None
    rfid = RFID(ip='', port='', com=com)
    if rfid.connect_serial():
        print("RFID VERSION:")
        print(rfid.get_version())

        print("RFID READ CARD:")
        print(rfid.get_card())

        rfid.close()