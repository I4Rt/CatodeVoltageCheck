class AskDevice:
    
    READ_BYTE = b'\x01'
    
    def __init__(self, recId:bytes, devId:bytes) -> None:
        self.recId = recId
        self.devId = devId
        