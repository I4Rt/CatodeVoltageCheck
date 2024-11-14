from model.static.ConnectionHolder import ConnectionHolder
from model.plant.MeasuringDevice import MeasuringDevice
import serial
if __name__ == "__main__":
    
    
    ConnectionHolder.changePort('COM9', baudrate=9600, timeout=1, parity='N')
    ser = ConnectionHolder.getConnection()
    md = MeasuringDevice(b'\x02', b'\x07')
    res = md.readData(ser)
    print(res)