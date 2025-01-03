from model.data.BaseData import *
from model.data.EventDB import *


class CommandDeviceDB(BaseData):
    __tablename__ = 'command_device_db'
    
    recId = Column(Integer, nullable=False)
    devId = Column(Integer, nullable=False)
    isActive = Column(Boolean, nullable=False)
    
    events = relationship('EventDB', cascade="all,delete", backref='command_device_db', lazy='select')
    
    __table_args__ = (UniqueConstraint('recId', 'devId'), )
    
    def __init__(self, recId:bytes|int, devId:bytes|int, isActive=False, id=None):
        super().__init__(id)
        if type(recId) == int:
            self.recId = recId
        elif type(recId) == bytes:
            self.recId = int.from_bytes(recId, byteorder='big')
        else:
            raise Exception('Wrong recId type')
        
        if type(devId) == int:
            self.devId = devId
        elif type(devId) == bytes:
            self.devId = int.from_bytes(devId, byteorder='big')
        else:
            raise Exception('Wrong recId type')
        self.isActive=isActive
        
    def setActive(self):
        self.isActive = True
        self.save()
        
    def setNotActive(self):
        self.isActive = False
        self.save()
    
    @classmethod
    def getByRecDevId(cls, recId, devId):
        with DBSessionMaker.getSession() as ses:
            return ses.query(cls).filter(
                        cls.recId == recId,
                        cls.devId == devId  
                    ).first()
    
    def _addChangeEvent(self, value):           # TODO: move this method away
        try:
            event = EventDB('change', value, time(), self.id)
            event.save()
            return True
        except Exception as e:
            print(e)
            pass
        return False
    
    def _addSwithcOffOnEvent(self, value:bool):           # TODO: move this method away
        try:
            if type(value) == bool:
                event = EventDB('swithc', int(value), time(), self.id)
                event.save()
                return True
            return False
        except Exception as e:
            print(e)
            pass
        return False
    
    
    def getEventsInLastDay(self) -> list[EventDB]:
        SECONDS_PER_DAY = 86400
        with DBSessionMaker.getSession() as ses:
            return ses.query(EventDB).filter(
                        EventDB.command_device_id == self.id,
                        EventDB.time_seconds > time() - SECONDS_PER_DAY
                    ).order_by(EventDB.id).all()
            
            
    def getLastEvent(self, eventType:str) -> EventDB:
        
        with DBSessionMaker.getSession() as ses:
            return ses.query(EventDB).filter(
                        EventDB.command_device_id == self.id,
                        EventDB.event_type == eventType
                    ).order_by(desc(EventDB.id)).first()
    
    def __parseTime(t):
        strftime('%Y-%m-%d %H:%M:%S', localtime(t))
        
    def getParamsList(self):
        return {'id': self.id, 
                'recId': self.recId,
                'devId': self.devId,
                'isActive': self.isActive,                
                }