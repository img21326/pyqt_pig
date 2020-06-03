from device_class.water_device import Water
if __name__ == "__main__":
    import sys
    try:
        com = sys.argv[1]
    except:
        com = None
    water = Water(ip='', port='', com=com)
    print(water.get_value())