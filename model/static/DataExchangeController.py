from config import *
from serial import Serial
from model.abstracts.Threadable import *
from model.CommandDevice import *
from model.static.ConnectionHolder import *


class DataExchangeController(Threadable):
    
    __TASK_TIMEOUT          = 10  # in seconds
    __RESERVE_TIMEOUT       = 0.5 # in seconds
    
    __MAX_QUEUE = 200
    
    __instance = None
    
    def __init__(self):
        ConnectionHolder.changePort(SERIAL_NAME)
        self.serial = ConnectionHolder.getConnection()
        # print(self.serial)
        # if self.serial is None:
        #     raise Exception('Wrong serial connection: None')
        self.__taskQueue   = []
        self.__resultQueue = {}
        
        
        self._thread = StopableThread(target=self.__workflow, looped=True)
        
        
    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance
    
    
    def __workflow(self) -> None:
        try:
            task = self.__taskQueue.pop()
            if time() - task['birth_time'] < self.__TASK_TIMEOUT:
                if self.serial:
                    res = self.__processTask(self.serial, task)
                    self.__resultQueue[task['id']] = res
                    lastKeys = list(self.__resultQueue.keys())[-200:] # TODO: check bugs, optimize
                    for k in self.__resultQueue:
                        if not(k in lastKeys):
                            self.__resultQueue.pop(k)
                else:
                    print('Workflow: Reseting connection', SERIAL_NAME)
                    ConnectionHolder.changePort(SERIAL_NAME)
                    self.serial = ConnectionHolder.getConnection()
                    
                # self.__resultQueue = self.__resultQueue[-200:] # TODO: check bugs
        except IndexError:
            pass
        except Exception as e:
            print('Workflow:', type(e), e)
        sleep(0.1)
    
    @staticmethod  
    def __getNewID():
        return int(time() * 1000)
    
    @staticmethod
    def __processTask(ser:Serial, task:dict) -> bool:
        try:
            
            if task['task_type'] == 'send_change':
                device:CommandDevice = task['device']
                setTime              = task['time']
                if setTime >= 0:
                    return device.sendOpenCommand(ser, abs(setTime))
                return device.sendCloseCommand(ser, abs(setTime))
                
        except Exception as e:
            print('DataExchangeController:', type(e), e)
        return False
    
    
    def addTask(self, device:CommandDevice, task_type:str, value:int=0) -> tuple[bool, int|None, float|None]:
        '''
        returns:
            res: result bool status
            id: task id to search thrue results
            timeout: time up to what it is nessesory to check task result
        '''
        passed = False
        id_ = self.__getNewID()
        time_ = time()
        task = {
                'device':     device,
                'task_type':  task_type,
                'birth_time': time_,
                'id':         id_
            }
        
        if task_type == 'send_change':
            task['time']      = int(value)
            passed = True
        # elif # TODO: if ness
    
        if passed:
            self.__taskQueue.append(task)
            return True, id_, time_ + self.__TASK_TIMEOUT + self.__RESERVE_TIMEOUT
        return False, None, None
    
    
    def getResult(self, id_, time_) -> bool:
        while time() < time_ :
            if id_ in self.__resultQueue:
                print(self.__resultQueue[id_])
                return self.__resultQueue[id_]
            sleep(0.1)
        
        return None

    
    

    
    