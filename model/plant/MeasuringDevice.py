

from model.plant.AskDevice import AskDevice
from tools.AskInterfaceTool import *
from serial import Serial
class MeasuringDevice(AskDevice):
    
    def __init__(self, recId: bytes, devId: bytes) -> None:
        super().__init__(recId, devId)
        self.deviceType = b'\x06'
        
    def readData(self, ser: Serial):
        '''
        returns:
            res:     bool
            code:    int
            voltage: int
            resist:  int
            
        codes:
             0,  'Нормальный ответ, парсинг выполнен'
            -1,  'Слишкий малый размер ответа'
            -2,  'Слишкий большой размер ответа'
            -3,  'Ошибка в сообщении'
            -4,  'Неизвестная форма овтета'
            -5,  'Ответ несовпадает запрашиваемым ID устрйоства'
        '''
        message = self.recId + self.devId + self.READ_BYTE + self.deviceType
        size, answer = sendMessage(ser, message)
        res, code, voltage, resist =  self.parseAnswer(size, answer)
        return res, code, voltage, resist
        
        
        
    
    def parseAnswer(self, size:int, answer:bytes) -> tuple[bool, int, float|None, int|None]:
        '''
        returns:
            res:     bool
            code:    int
            voltage: float
            resist:  int
            
        codes:
             0,  'Нормальный ответ, парсинг выполнен'
            -1,  'Слишкий малый размер ответа'
            -2,  'Слишкий большой размер ответа'
            -3,  'Ошибка в сообщении'
            -4,  'Неизвестная форма овтета'
            -5,  'Ответ несовпадает запрашиваемым ID устрйоства'
        '''
        
        if self.recId == answer[0:1] and self.devId == answer[1:2]:
            if size < 11:
                return False, -1, None, None
            res, code, msg =  checkAnswer(size, answer)
            if res:
                return True, 0, hexToInt(answer[5:7])/10, hexToInt(answer[7:9])
            return False, code, None, None
        return False, -5, None, None
        
    
    
