from itertools import product
from ttlsap.adapter.spcyx2 import get_spcyx_data
from ttlsap.sa_eng_spcyx import SpcYxApi
from tools.redis_db import RedisDb
from tools.logger import Logger
from tools.innodrive import InnoDrive
from model.model import chart_id_list, spc_data_info
import base64
import os



def test_request_handler_get_spcyx_data():

	""" info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""
	

	redis = RedisDb.default()
	cache_key_text = "/ds/eng/spcyx/tft7/438N/MB_X/TJDF40XK/DF40XK_A5_4/4300/?start_time=20220712080000&end_time=20220712170000&run_mode=normal&owner_code=crn0&peqpt=TLCD0300"
	cache_key = base64.b64encode(cache_key_text.encode('ascii'))
	redis.set(cache_key,"init")
	fab = "T7"
	chart_list = ""
	token = ""
	start_dttm = "2022-07-12 08:00:00"
	end_dttm = "2022-07-12 17:00:00"
	method = ""
	product = "TJDF40XK"
	pproc_id="4300"
	peqpt_id="TLCD0300"
	precipe_id = "DF40XK_A5_4_254A"
	owner_code = "CRN0"
	run_mode = "N"
	spc_item_id = "MB_X"
	proc_id = "438N"
	info = spc_data_info(fab=fab, chart_list=chart_list, token=token, start_dttm=start_dttm, end_dttm=end_dttm, method=method, 
	product=product,pproc_id=pproc_id, peqpt_id=peqpt_id, precipe_id=precipe_id, owner_code=owner_code,
	run_mode= run_mode, spc_item_id=spc_item_id, proc_id=proc_id)
	
	Logger.log(f"get_spc_data info: {info} with cache key {cache_key}")
	dset= get_spcyx_data(info, cache_key)
	Logger.log(f"result: {dset}")

def test_spcyxapi():
	spcyx = SpcYxApi(nd='/ds/eng/spcyx',fab='TFT7',proc_id='438N',item='MB_X',prod='TJDF40XK',
		recipe='DF40XK_A5_4_254A',pproc_id='4300',start_time='20220802080000',end_time='20221222170000',
		run_mode='N', owner_code='CRN0', peqpt='TLCD0300', clientid='eng')
	assert spcyx.cache_key_text == '/ds/eng/spcyx/T7/438N/MB_X/TJDF40XK/DF40XK_A5_4_254A/4300?start_time=2022-08-02 08:00:00&end_time=2022-12-22 17:00:00&run_mode=N&owner_code=CRN0&peqpt=TLCD0300'
	spcyx.spcyxbytime()
	spcyx.save_clientdatastore()
	spcyx.save_clientdatastore(asciifilename=True)