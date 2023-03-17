from itertools import product
from ttlsap.adapter.spcyx2 import get_spcyx_data
from ttlsap.sa_eng_spcyx import SpcYxApi
from tools.redis_db import RedisDb
from tools.logger import Logger
from tools.innodrive import InnoDrive
from model.model import chart_id_list, spc_data_info
import base64
import os
from tests.auxinfo import SpcYxInfo, casttime1

def test_request_handler_get_spcyx_data():

	""" info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""

	casefilepath = os.path.join('tests/doc/testcases', 'spcyx-testcases.json')
	ts = SpcYxInfo(casefilepath,'spcyx1')
	tc = ts._info
	tc.start_dttm_c1 = casttime1(tc.start_dttm)
	tc.end_dttm_c1 = casttime1(tc.end_dttm)
	redis = RedisDb.default()
	# cache_key_text = "/ds/eng/spcyx/tft7/438N/MB_X/TJDF40XK/DF40XK_A5_4/4300/?start_time=20220712080000&end_time=20220712170000&run_mode=normal&owner_code=crn0&peqpt=TLCD0300"
	cache_key_text = f"/ds/eng/spcyx/{tc.fab}/{tc.proc_id}/{tc.spc_item_id}/{tc.product}/{tc.precipe_id}/{tc.pproc_id}/?start_time={tc.start_dttm_c1}&end_time={tc.end_dttm_c1}&run_mode={tc.run_mode}&owner_code={tc.owner_code}&peqpt={tc.peqpt_id}"
	cache_key = base64.b64encode(cache_key_text.encode('ascii'))
	redis.set(cache_key,"init")
	fab = tc.fab
	chart_list = tc.chart_list
	token = ""
	start_dttm = tc.start_dttm
	end_dttm = tc.end_dttm
	method = tc.method
	product = tc.product
	pproc_id= tc.pproc_id
	peqpt_id= tc.peqpt_id
	precipe_id = tc.precipe_id
	owner_code = tc.owner_code
	run_mode = tc.run_mode
	spc_item_id = tc.spc_item_id
	proc_id = tc.proc_id
	info = spc_data_info(fab=fab, chart_list=chart_list, token=token, start_dttm=start_dttm, end_dttm=end_dttm, method=method, 
	product=product,pproc_id=pproc_id, peqpt_id=peqpt_id, precipe_id=precipe_id, owner_code=owner_code,
	run_mode= run_mode, spc_item_id=spc_item_id, proc_id=proc_id)
	
	Logger.log(f"get_spc_data info: {info} with cache key {cache_key}")
	dset= get_spcyx_data(info, cache_key)
	Logger.log(f"result: {dset}")

def on_spcyxapi(testcase):
	casefilepath = os.path.join('tests/doc/testcases', 'spcyx-testcases.json')
	ts = SpcYxInfo(casefilepath,testcase)
	tc = ts._info
	tc.start_dttm_c1 = casttime1(tc.start_dttm)
	tc.end_dttm_c1 = casttime1(tc.end_dttm)
	tc.fab_pub = SpcYxApi.convert_fab_format(tc.fab, reverse=True)

	spcyx = SpcYxApi(nd='/ds/eng/spcyx',fab=tc.fab_pub,proc_id=tc.proc_id,item=tc.spc_item_id,prod=tc.product,
		recipe=tc.precipe_id,pproc_id=tc.pproc_id,start_time=tc.start_dttm_c1,end_time=tc.end_dttm_c1,
		run_mode=tc.run_mode, owner_code=tc.owner_code, peqpt=tc.peqpt_id, clientid='eng')
	assert spcyx.cache_key_text == f'/ds/eng/spcyx/{tc.fab}/{tc.proc_id}/{tc.spc_item_id}/{tc.product}/{tc.precipe_id}/{tc.pproc_id}?start_time={tc.start_dttm}&end_time={tc.end_dttm}&run_mode={tc.run_mode}&owner_code={tc.owner_code}&peqpt={tc.peqpt_id}'
	result = spcyx.spcyxbytime()
	if result["status"] == 200: spcyx.save_clientdatastore(h5=False)
	else : print(result)

def test_spcyxapi(testcase='spcyx2'):
	on_spcyxapi(testcase)