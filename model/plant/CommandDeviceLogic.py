from model.plant.AskDevice import AskDevice
from tools.AskInterfaceTool import *
from serial import Serial


class CommandDeviceLogic(AskDevice):
    _MAX_VALUE = 58000
    _MIN_VALUE = 0
    def __init__(self, recId: bytes, devId: bytes) -> None:
        super().__init__(recId, devId)
        self.deviceType = b'\x05'
        
    def sendOpenCommand(self, ser: Serial, time:int): 
        
        '''
        returns:
            res: bool
        '''
        message = self._devId + self.OPEN_BYTE + time.to_bytes(2, byteorder='big')
        print('open message', message)
        size, answer = sendMessage(ser, message)
        print('open answer', answer)
        return message in answer
    
    def sendCloseCommand(self, ser: Serial, time:int): 
        
        '''
        returns:
            res: bool
        '''
        message = self._devId + self.CLOSE_BYTE + time.to_bytes(2, byteorder='big')
        print('close message', message)
        size, answer = sendMessage(ser, message)
        print('close answer', answer)
        return message in answer
