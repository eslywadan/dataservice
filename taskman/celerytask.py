from celery import Celery
from celery.result import AsyncResult
from ttlsap.sa_eng import EdcRawApi
from ttlsap.sa_eng_spcyx import SpcYxApi
from tools.clientdatastore import ClientDataStore
from tools.celery_oper import *
import time
from tools.logger import Logger
from taskman.celeryapp import app
import os
import json


app = app
@app.task
def add(x, y):
    time.sleep(3)
    print()
    return x + y

@app.task
def edcrawbytime(**kwargs):
    edcrawapi = EdcRawApi()
    res = edcrawapi.edcrawbytime(fab=kwargs['fab'],equip=kwargs['equip'],edc=kwargs['edc'],start_time=kwargs['start_time'],
        	end_time=kwargs['end_time'],sub_eq=kwargs['sub_eq'],grp_id='')

    return res


@app.task
def save_edcrawbytime_cds(taskid, clientid, filename,timeout=30):
    """"The function has a delay work on waiting the completion of input task id
        If the input task is 'SUCCESS', it will proceed to get the result by the taskid and save it to the client's data store
    """
    
    state = chk_async_task(taskid, timeout)
    if state['Success Task'] is not None and taskid in state['Success Task'] : 
        res = AsyncResult(taskid, app=app)
        data = res.result
        Logger.log(f"branch task to monitor the state of {taskid} requested by client {clientid} has res:")
        Logger.log(data)
        Logger.log(f'saved file name {filename}')
        filepath = os.path.join("temp",filename)
        filecontent = json.dumps(data, indent=4)
        with open(filepath,'w') as f:
            f.write(filecontent)
        cds = ClientDataStore(clientid=clientid)
        cds.put_file(sfilepath=filepath,sfilename=filename,
        tsubpath=taskid,tfilename=filename)
        
    else: return{"time out":f"save result task has time out for {timeout} secs"}


@app.task
def spcyxbytime(**kwargs):
    spcyx = SpcYxApi(fab=kwargs['fab'], proc_id=kwargs['proc_id'], item=kwargs['item'], prod=kwargs['prod']
            ,recipe=kwargs['recipe'], pproc_id=kwargs['pproc_id'],start_time = kwargs['start_time'],
            end_time = kwargs['end_time'], run_mode = kwargs['run_mode'],owner_code = kwargs['owner_code']
            ,peqpt = kwargs['peqpt'], clientid=kwargs['clientid'], nd=kwargs['nd'])
    res = spcyx.spcyxbytime()
    spcyx.save_clientdatastore()
    return res

def async_add(x, y):
    receipt = add.delay(x, y)
    return receipt.id
    
def async_edcrawbytime(**kwargs):
    receipt1 = edcrawbytime.delay(fab=kwargs['fab'],equip=kwargs['equip'],edc=kwargs['edc'],start_time=kwargs['start_time'],
        	end_time=kwargs['end_time'],sub_eq=kwargs['sub_eq'],grp_id='')
    filename = kwargs['saved_filename']
    receipt2 = save_edcrawbytime_cds.delay(receipt1.id, kwargs['clientid'], filename)        
    return receipt1.id

def async_spcyxbytime(**kwargs):
    receipt = spcyxbytime.delay(fab=kwargs['fab'], proc_id=kwargs['proc_id'], item=kwargs['item'], prod=kwargs['prod']
            ,recipe=kwargs['recipe'], pproc_id=kwargs['pproc_id'],start_time = kwargs['start_time'],
            end_time = kwargs['end_time'], run_mode = kwargs['run_mode'],owner_code = kwargs['owner_code']
            ,peqpt = kwargs['peqpt'], clientid=kwargs['clientid'], nd=kwargs['nd'])
    return receipt.id

def get_asyncresult(id):
    result = AsyncResult(id)
    if result.state == "SUCESS":
        return result.result
    else:
        return result.state

