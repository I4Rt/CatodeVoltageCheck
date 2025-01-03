from config import *



from model.CommandDevice import *
from web_controllers.PageController import *
from web_controllers.RestController import *

from  model.static.DeviceStatuser import *





if __name__ == "__main__":
    
    Base.metadata.create_all(e)
    
    
    # statuser.startThread()
    
    with app.app_context():
        ConnectionHolder.changePort(SERIAL_NAME)
        # ser = ConnectionHolder.getConnection()
        # print(ser)
        
        DataExchangeController.getInstance().startThread()
        
        deviceStatuser = DeviceStatuser.getInstance()
        deviceStatuser.loadDevices()
        
        app.run(host='0.0.0.0', port=3031, debug=False) # TODO: change debug on false in prod
        
    DataExchangeController.getInstance().stopThread()
    # statuser.stopThread()
    
    
    # 
    
    # ser = ConnectionHolder.getConnection()
    # cd = CommandDevice.getByID(1)
    
    # print(cd._devId, cd.devId)
    
    # res = cd.sendOpenCommand(ser, 2000)
    
    # res = cd.sendCloseCommand(ser, 2000)
    