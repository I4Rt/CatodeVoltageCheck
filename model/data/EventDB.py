from model.data.BaseData import *

class EventDB(BaseData):
    __tablename__ = 'event_db'
    
    value = Column(Double, nullable=False)
    event_type = Column(String, nullable=False)
    time_seconds = Column(Integer, nullable=False) # uinttime
    
    
    command_device_id = Column(Integer, ForeignKey('command_device_db.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, valType:str, val:float, t:int, command_device_id:int, id=None):
        super().__init__(id)
        self.event_type = valType
        self.value = val
        self.time_seconds = t
        self.command_device_id = command_device_id
        
    def getParamsList(self):
        return {
            # 'command_device_id': self.command_device_id,
            'event_type':        self.event_type,
            'value':             self.value,
            'time_seconds':      self.time_seconds,
            # 'id': self.id
        }
        
    