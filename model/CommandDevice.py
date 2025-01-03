from model.data.CommandDeviceDB import *
from model.plant.CommandDeviceLogic import *

class CommandDevice(CommandDeviceDB, CommandDeviceLogic):
    
    def __init__(self, recId:int, devId:int, id=None):
        CommandDeviceDB.__init__(self, recId, devId, id)
        CommandDeviceLogic.__init__(self, 
                                      recId.to_bytes(1, byteorder='big'), 
                                      devId.to_bytes(1, byteorder='big')
                                      )
        self.id=id # TODO: check the bug

        
    @classmethod        
    def DBDeviceAdapter(cls, mddb:CommandDeviceDB):
        return cls(mddb.recId, mddb.devId, mddb.id)
    
    @classmethod
    def getLast(cls) -> "CommandDevice":
        return cls.DBDeviceAdapter(CommandDeviceDB.getLast())
    
    @classmethod
    def getAll(cls) -> list["CommandDevice"]:
        return list(map(lambda x: cls.DBDeviceAdapter(x), CommandDeviceDB.getAll()))
    
    @classmethod
    def getByID(cls, id:int) -> "CommandDevice":
        return cls.DBDeviceAdapter(CommandDeviceDB.getByID(id))
    
    @classmethod
    def getByDevRecId(cls, recId:int, devId:int) -> "CommandDevice":
        return cls.DBDeviceAdapter(CommandDeviceDB.getByRecDevId(recId, devId))
    
    def addChangeEvent(self, value):
        return self._addChangeEvent(min(self._MAX_VALUE, max(value, self._MIN_VALUE)))