from time import time, sleep
from model.abstracts.Threadable import *
# from model.abstracts.SingletonLike import *

class RuntimeStatuser(Threadable):
    
    __TMP_FILE_NAME = 'run.tmp'
    __ERROR_INTERVAL = 2*60    # in seconds
    __SAVE_INTERVAL = 10       # in seconds
    
    __instance = None

    def __workflow(self):
        startTime = time()
        with open(self.__TMP_FILE_NAME, 'w+') as f:
            lastTime = 0
            try:
                lastTime = int(f.read())
            except:
                pass
            nowTime = time()
            if nowTime - lastTime > self.__ERROR_INTERVAL:
                self.__consistenced = False # consistenced = согласованный
            f.write(str(int(nowTime)))

        sleep(self.__SAVE_INTERVAL - (time() - startTime))
        
    
    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance
        
    def __init__(self):
        self.__consistenced = False
        self._thread = StopableThread(target=self.__workflow, looped=True)
    
    def isConsistenced(self) -> bool:
        return self.__consistenced
    
    def setConsistenced(self) -> None:
        self.__consistenced = True
