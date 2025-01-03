from tools.StopableThread import *

class Threadable:
    
    def __init__(self):
        self._thread:StopableThread = None
    
    def isWorking(self)  -> bool:
        return self._thread.is_alive()
    
    def startThread(self) -> True:
        self._thread.start()
        
    def stopThread(self):
        self._thread.stop()
        self._thread.join()