from model.CommandDevice import *

class DeviceStatuser:
    
    __instance = None
    
    def __init__(self):
        self.__deviceСonsistencedStatusDict = {} # consistenced = согласованный
                                                 # True  - согласованн
                                                 # False - рассогласованн
                                                                 
    @classmethod
    def getInstance(cls) -> "DeviceStatuser":
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance
    
        
    def loadDevices(self, ) -> None:
        devices = CommandDevice.getAll()
        self.__deviceСonsistencedStatusDict = {device.id:False for device in devices}
        print('\n\n__deviceСonsistencedStatusDict',self.__deviceСonsistencedStatusDict)
        
        
    def setAllDevicesUnconsistenced(self):
        for devId in self.__deviceСonsistencedStatusDict:
            self[devId] = False
        
        
    def addDevice(self, device:CommandDevice) -> None:
        if device.id == None:
            return False
        self.__deviceСonsistencedStatusDict[device.id] = False
        return True
        
        
    def setDeviceСonsistenced(self, id_:int) -> bool:
        if id_ in self.__deviceСonsistencedStatusDict:
            self.__deviceСonsistencedStatusDict[id_] = True
            print('\n\n__deviceСonsistencedStatusDict',self.__deviceСonsistencedStatusDict)
            return True
        return False
    
    
    def setDeviceUnconsistenced(self, id_:int) -> bool:
        if id_ in self.__deviceСonsistencedStatusDict:
            self.__deviceСonsistencedStatusDict[id_] = False
            return True
        return False
    
    
    def getDeviceStatus(self, id_:int) -> bool|None:
        print('\n\n__deviceСonsistencedStatusDict',self.__deviceСonsistencedStatusDict)
        if id_ in self.__deviceСonsistencedStatusDict:
            return self.__deviceСonsistencedStatusDict[id_]
        return None