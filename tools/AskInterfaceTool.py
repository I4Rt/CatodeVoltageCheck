import serial

from tools.crc.crc16module import *
from tools.byteTools.ByteTools import *

def sendMessage(ser:serial.Serial, message):
        message_crc = add_crc(message, reversed=True)
        ser.write(message_crc)
        ser.flush()
        size, answer = byte_reader(ser, 10)
        return size, answer
    
def checkAnswer(size, answer:bytes):
    '''
    codes:
         0,  'Нормальный ответ'
        -1,  'Слишкий малый размер ответа'
        -2,  'Слишкий большой размер ответа'
        -3,  'Ошибка в сообщении'
        -4,  'Неизвестная форма овтета'
    '''
    if size < 3:
        return False, -1, 'Слишкий малый размер ответа'
    if size > 11:
        return False, -2, 'Слишкий большой размер ответа'
    if answer[2:3]  == b'\x04':
        return False, -3,  'Ошибка в сообщении'
    if answer[2:3]  != b'\x04' and answer[2:3]  != b'\x01':
        return False, -4,  'Неизвестная форма овтета'
    return True, 0, 'Нормальный ответ'