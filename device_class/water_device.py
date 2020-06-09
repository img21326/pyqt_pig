import serial
import time
from logs.logger import log

try:
    from device_class.device import Device
except:
    from device import Device


class Water(Device):

    READ_COMMAND = [0x2a, 0x00, 0x00, 0x01, 0x00, 0xff, 0x00, 0xff, 0x11, 0xee]

    def get_value(self):
        if self.connect_serial():
            r = self.write(self.READ_COMMAND, 2.8)
            # print(r)
            r = r[30:]
            r = r[:26]

            bval = r[1:10]
            bval.reverse()
            sval = ""
            ival = 0

            bop = r[-2:]
            sop = ""
            iop = 0

            xval = r[13:]
            xval = xval[1:10]
            xval.reverse()
            sxval = ""
            ixval = 0

            xop = r[-2:]
            sxop = ""
            ixop = 0

            for i in bval:
                i = i.decode()
                sval += i

            for o in bop:
                o = o.decode()
                sop += o

            iop = int(sop)                
            ival = float(sval) * (10 ** iop)

            for x in xval:
                x = x.decode()
                sxval += x
            
            for xo in xop:
                xo = xo.decode()
                sxop += xo
            
            ixop = int(sxop)
            ixval = float(sxval) * (10 ** ixop)

            return ival - ixval
        else:
            log('error', "WATER_DEVICE: not connect device")
            print("WATER_DEVICE: not connect device")
            return None
