from config import *

from model.CommandDevice import *
from model.data.EventDB import *

from model.static.DeviceStatuser import *

from flask import request, url_for, redirect, render_template

@app.route('/', methods=['GET'])
def redirectMainPage():
    return redirect('main')


@app.route('/main', methods=['GET'])
def getMainPage():
    vault_devices = CommandDevice.getAll()
    deviceData = []
    for device in vault_devices:
        devData = {}
        devData['info'] = device.getParamsList()
        
        if DeviceStatuser.getInstance().getDeviceStatus(device.id) is None:
            DeviceStatuser.getInstance().addDevice(device)
        devData['is_consistenced'] = DeviceStatuser.getInstance().getDeviceStatus(device.id)
        
        lastEvent = device.getLastEvent(eventType='change')
        devData['last_change_event'] = None
        try:
            devData['last_change_event'] = lastEvent.getParamsList()
        except Exception as e:
            print(type(e), e)
            pass
        plotData = device.getEventsInLastDay()
        devData['plot_data'] = []
        try:
            for event in plotData:
                if event.event_type == 'change':
                    eventData = event.getParamsList()
                    devData['plot_data'].append(eventData)
        except:
            pass
        deviceData.append(devData)
        
        
    return render_template('main.html', devices_data=deviceData)