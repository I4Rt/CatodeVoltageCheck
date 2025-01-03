import serial
from time import time

def byte_reader(ser: serial.Serial, size = 10):
    buf = b''
    while True:
        res = ser.read()
        # print(res)
        if res:
            buf += res
            if len(buf) > 72:
                ser.close()
                ser.open()
                return len(buf), buf
                # raise Exception(str(buf))
            continue
        break 

    
    return len(buf), buf


def hexToInt(hex:bytes):
    return int.from_bytes(hex, byteorder='big')