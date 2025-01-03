class AskDevice:
    
    READ_BYTE  = b'\x01'
    
    OPEN_BYTE  = b'\x01'
    CLOSE_BYTE = b'\x02'
    
    def __init__(self, recId:bytes, devId:bytes) -> None:
        self._recId = recId # unnecessary
        self._devId = devId
