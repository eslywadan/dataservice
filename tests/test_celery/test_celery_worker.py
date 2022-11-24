from multiprocessing.connection import wait
import random
from taskman.celerytask import *
from tools.logger import Logger
import random
import time
from celery.result import AsyncResult
from tests.auxinfo import TrailArg
import datetime
from tools.celery_oper import *


def submit_edcraw_task():
	resp = submit_tasks_start(app, 'taskman.celerytask.edcrawbytime')
	if 0 in resp.keys(): return {'Warning':'No available worker!'}
	ta = TrailArg('edcrawasync1')   # ta stands for 'trail arguments'
	r = {}
	i = 0
	date_format = '%Y-%m-%d %H:%M:%S:%f'
	while i < ta.args['req_count']:
		r[i] = async_edcrawbytime(fab=ta.args['fab'],equip=ta.args['equip'],edc=ta.args['item'],start_time=ta.args['start_time'],
        	end_time=ta.args['end_time'],sub_eq=ta.args['sub_equip'],grp_id='', saved_filename=ta.args['saved_filenanme'],clientid=ta.args['clientid'])
		print(r[i])
		i += 1

	return r

def submit_spcyx_task():
	resp = submit_tasks_start(app, 'taskman.celerytask.spcyxbytime')
	if 0 in resp.keys(): return {'Warning':'No available worker!'}
	ta = TrailArg('spcyxasync1')   # ta stands for 'trail arguments'
	return async_spcyxbytime(fab=ta.args['fab'], proc_id=ta.args['proc_id'], item=ta.args['spc_item_id'], prod=ta.args['product']
            ,recipe=ta.args['precipe_id'], pproc_id=ta.args['pproc_id'],start_time = ta.args['start_dttm'],
            end_time = ta.args['end_dttm'], run_mode = ta.args['run_mode'],owner_code = ta.args['owner_code']
            ,peqpt = ta.args['peqpt_id'], clientid=ta.args['clientid'], nd=ta.args['nd'])


def submit_add_tasks():
	resp = submit_tasks_start(app, 'taskman.celerytask.add')
	if 0 in resp.keys(): return {'Warning':'No available worker!'} 
	r = {}
	for i in range(10):
		x = random.randint(-100,100)
		y = random.randint(-100,100)
		x += random.randint(-10,10)
		y += random.randint(-10,10)
		r[i] = async_add(x,y)
		print(r[i])

	return r


def test_add_celery():
	rs_add =  submit_add_tasks()
	assert len(rs_add) == 10
	time.sleep(1)
	


def test_edcraw_celery():
		rs_edcraw = submit_edcraw_task()
		assert len(rs_edcraw) == 1
		time.sleep(3)
		async_edcraw = chk_async_tasks(rs_edcraw)

def test_spcyx_celery():
		rs_spcyx = submit_spcyx_task()
		time.sleep(10)
		async_spcyx = chk_async_task(rs_spcyx)
