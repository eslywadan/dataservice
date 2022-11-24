import re
from tools.logger import Logger
from celery.result import AsyncResult
from taskman.celeryapp import app
import time


def get_worker_status(app:app,items='all'):
	i = app.control.inspect()
	if items == 'all' or items == 'availability': availability = i.ping()
	else: availability = None
	if items == 'all' or items == 'stats': stats = i.stats()
	else: stats = None
	if items == 'all' or items == 'registered_tasks': registered_tasks = i.registered()
	else: registered_tasks = None
	if items == 'all' or items == 'active_tasks': active_tasks = i.active()
	else: active_tasks = None
	if items == 'all' or items == 'scheduled_tasks': scheduled_tasks = i.scheduled()
	else: scheduled_tasks = None
	result = {
		'availability':availability or None,
		'stats':stats or None,
		'registered_tasks':registered_tasks or None,
		'active_tasks':active_tasks or None,
		'scheduled_tasks':scheduled_tasks or None
	}

	return result


def assure_task_has_registered_worker(app:app, task):
    reg_tasks = get_worker_status(app,items='registered_tasks')['registered_tasks']
    if reg_tasks == None : return {0:f'submit task {task} has not registerd worker'}
    
    reg_worker = []
    for worker in reg_tasks:
        if task in reg_tasks[worker]:reg_worker.append(worker)
    if len(reg_worker) == 0: return {0:f'submit task {task} has not registerd worker'}
    else: return {1:reg_worker}


def submit_tasks_start(app:app, task):
	broker_url = app._conf['broker_url']
	result_url = app._conf['result_backend']
	Logger.log(f'{__name__}: test celery broker_url:{broker_url}')
	Logger.log(f'{__name__}: test celery result_url:{result_url}')
	resp = assure_task_has_registered_worker(app, task)
	return resp


def chk_async_tasks(tasks:dict, timeout=10):
	
    rs = tasks
    st = {}
    wait = 0
    while st.__len__() < rs.__len__() and wait <=timeout:
        for rid in rs:
            if AsyncResult(rs[rid], app=app).state == 'SUCCESS':
                st.update({rid:rs[rid]})
        time.sleep(0.2)
        wait += 0.2
    
    for task in st: rs.pop(task)
    
    return {'Tasks':tasks, 'Success Task':st, 'Remain Task':rs, 'Wait time': wait}



def chk_async_task(task, timeout=10):
	wait = 0
	st = None
	rs = None
	while AsyncResult(task, app=app).state != 'SUCCESS' and wait <= timeout:
		time.sleep(1)
		wait += 1
	if AsyncResult(task).state == 'SUCCESS': st=task
	elif AsyncResult(task).state != 'SUCCESS': rs=task
	
	return {'Tasks':task, 'Success Task':st, 'Remain Task':rs, 'Wait time': wait}


def get_async_result(task, timeout=10):
	wait = 0
	st = None
	rs = None
	asyncres = AsyncResult(task, app=app) 
	while asyncres.state != 'SUCCESS' and wait <= timeout:
		time.sleep(1)
		wait += 1
		asyncres = AsyncResult(task, app=app)

	if asyncres.state == 'SUCCESS': 
		st=task
		res = asyncres.result
		return {'Tasks':task, 'Success Task':st, 'Result':res, 'Wait time': wait}

	elif asyncres.state != 'SUCCESS': 
		rs=task
		return {'Tasks':task, 'Remain Task':rs, 'Wait time': wait}

	