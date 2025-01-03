from config import *

from model.static.DeviceStatuser import *


from model.abstracts.DBSessionMaker import *
from model.CommandDevice import *
from model.data.EventDB import *
from web_controllers.web_tools.exception_processing import *

from model.static.DataExchangeController import *
from model.static.DeviceStatuser import *

import pandas as pd
import io
import zipfile

from flask import request, url_for, redirect, render_template, make_response, Response

@app.route('/getData', methods=['GET', 'POST'])
@cross_origin()
@exception_processing
def getEventsData():
    vaultId = int(request.args.get('vaultId'))
    vault = CommandDevice.getByID(vaultId)
    res_list = vault.getEventsInLastDay()
    
    return list(map(lambda x: x.getParamsList(), res_list))


@app.route('/addChangeEvent', methods=['GET', 'POST'])
@cross_origin()
@exception_processing
def addChangeEvent():
    
    vaultId = request.json['vaultId'] 
    value = int(request.json['value'])
    
    
    if DeviceStatuser.getInstance().getDeviceStatus(vaultId):
        device = CommandDevice.getByID(vaultId)
        if device:
            lastEvent = device.getLastEvent('change')
            if lastEvent:
                addTaskResult, task_id, timeout = DataExchangeController.getInstance().addTask(device, 'send_change', value) # TODO: add busy status to except multuple lastevent-based sum with values in async request processing
                if addTaskResult:
                    sendTaskResult = DataExchangeController.getInstance().getResult(task_id, timeout)
                    print('task send:', sendTaskResult)
                    if sendTaskResult:
                        print(lastEvent.value, value, lastEvent.value + value)
                        dbSaveRes  = device.addChangeEvent(min(580000, max(lastEvent.value + value, 0)))
                        return {request.path: dbSaveRes}
    return {request.path: False}
    


@app.route('/resetVaultValue', methods=['GET'])
@cross_origin()
@exception_processing
def resetVault():
    GO_HOME_VALUE = -58000
    vaultId = int(request.args.get('vaultId'))
    device = CommandDevice.getByID(vaultId)
    if device:
        addTaskResult, task_id, timeout = DataExchangeController.getInstance().addTask(device, 'send_change', GO_HOME_VALUE)
        if addTaskResult:
            sendTaskResult = DataExchangeController.getInstance().getResult(task_id, timeout)
            if sendTaskResult:
                dbSaveRes  = device.addChangeEvent(0)
                if dbSaveRes:
                    res = DeviceStatuser.getInstance().setDeviceСonsistenced(vaultId)
                    return {request.path: res}
    return {request.path: False}

@app.route('/getEvents', methods=['GET'])
@cross_origin()
@exception_processing
def getEvents():
    ROW_COMBINE = 10000
    startTime = int(request.args.get('startTime'))
    endTime   = int(request.args.get('endTime'))
    data = []
    with DBSessionMaker.getSession() as ses:

        sqlQuery = f'''
            select 
                cd.id as device, 
                CONCAT(cd."recId", '_', cd."devId") as route, 
                ev.event_type,
                ev.time_seconds,
                ev.value
            from 
                event_db as ev 
                    right outer join 
                command_device_db as cd 
                    on ev.command_device_id = cd.id
            where 
                ev.time_seconds > {startTime} 
                and
                ev.time_seconds < {endTime}
            order by ev.time_seconds;
        '''
        res = ses.execute(text(sqlQuery))
        ses.commit()
        data = list(map( lambda row: row[:], res))
    
    zipFile = io.BytesIO()
    with zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED) as zf:
        i = 1
        for data_cut in [ data[i*ROW_COMBINE:(i+1)*ROW_COMBINE] for i in range(len(data)//ROW_COMBINE + (1 if len(data)%ROW_COMBINE else 0)) ]:
            df = pd.DataFrame(data_cut)
            zf.writestr(f'events_part_{i}.csv', df.to_csv(header=False))
            i+= 1
    zipFile.seek(0)
    
    return Response(zipFile.getvalue(),
                    mimetype='application/zip',
                    headers={'Content-Disposition': f'attachment;filename=events_export_{time()}.zip'})
