import re
from ttlsap.adapter.spcyx2 import get_spcyx_data
from tools.redis_db import RedisDb
from tools.logger import Logger
from tools.innodrive import InnoDrive
from tools.clientdatastore import ClientDataStore
from tools.config_loader import ConfigLoader
from model.model import chart_id_list, spc_data_info
import base64
import os
import time

class SpcYxApi:
	"""The class accept the request from front end and do required transform of parameters"""
	_redis = RedisDb.default()
	_input_time_format = '%Y%m%d%H%M%S'
	_output_time_format = '%Y-%m-%d %H:%M:%S'
	csvfilepath = None
	dataobjid = None
	b64csvfilename = None
	asciifilename = None

	def __init__(self,**kwargs):
		"""
			nd,           'name of data entity, ex. value = 'spcyx''  
			fab,          'ex. 'TFT8'' 
			proc_id,      'spc measure op id'  
			item,		  'spc item'
			prod,         'measure product'    
			recipe,       'measure recipe' 
			pproc_id,     'Previous manufacturing op is'
			start_time,   'when the manufacturing op was start' 
            end_time,     'when the manufacturing op was end' 
			run_mode,     'run_mode'
			owner_code,   'owner_code'
			peqpt,        'previous equipment id'
			clientid=None 'client id'
		"""
		fab = kwargs['fab']
		proc_id = kwargs['proc_id']
		item = kwargs['item']
		prod = kwargs['prod']
		recipe = kwargs['recipe']
		pproc_id = kwargs['pproc_id']
		start_time = kwargs['start_time']
		end_time = kwargs['end_time']
		run_mode = kwargs['run_mode']
		owner_code = kwargs['owner_code']
		peqpt = kwargs['peqpt']

		self.client = kwargs['clientid']
		self.dataname = kwargs['nd']
		self.set_info(fab,proc_id,item,prod,recipe,pproc_id, start_time,
            end_time,run_mode, owner_code, peqpt)

	def set_info(self,fab,proc_id,item,prod,recipe,pproc_id, start_time,
            end_time,run_mode, owner_code, peqpt):
		
		fab = SpcYxApi.convert_fab_format(fab)
		start_time = SpcYxApi.convert_time_format(start_time)
		end_time = SpcYxApi.convert_time_format(end_time)
		# run_mode = SpcYxApi.verify_run_mode(run_mode)
		# owner_code = SpcYxApi.verify_owner_code(owner_code)
		self.cache_key_text = f"{self.dataname}/{fab}/{proc_id}/{item}/{prod}/{recipe}/{pproc_id}?start_time={start_time}&end_time={end_time}&run_mode={run_mode}&owner_code={owner_code}&peqpt={peqpt}"
		self.cache_key = base64.b64encode(self.cache_key_text.encode('ascii'))
		self.info = spc_data_info(fab=fab, chart_list="chart_list", token="token", start_dttm=start_time, end_dttm=end_time, method="method", 
								product=prod,pproc_id=pproc_id, peqpt_id=peqpt, precipe_id=recipe, owner_code=owner_code,run_mode= run_mode, 
								spc_item_id=item, proc_id=proc_id)

	def spcyxbytime(self):
		
		self._redis.set(self.cache_key, "init")
		Logger.log(f"get_spc_data info: {self.info} with cache key {self.cache_key}")
		end_result = get_spcyx_data(self.info, self.cache_key)
		
		if end_result["status"] == 200:
			self.csvfilepath = end_result["csv file"][0]
			self.b64csvfilename = end_result["csv file"][1]
			self.h5filepath = end_result["hdf5 file"][0]
			self.b64h5filename = end_result["hdf5 file"][1]
		
		Logger.log(f"result: {end_result}")

		return end_result

	def save_clientdatastore(self, asciifilename=True, h5=True):
		clds = ClientDataStore(clientid=self.client)
		if asciifilename:
				filenameb = self.b64csvfilename
				filename = base64.b64decode(filenameb.split(".")[0][1:])
				ffilename = filename.decode("ascii")
		sourcefilepath = self.csvfilepath
		sourcefilename = self.b64h5filename
		targetsubpath = ffilename.split("?")[0]
		targetfilename = ffilename.split("?")[1]
		resp = clds.put_file(sfilepath=sourcefilepath, sfilename=sourcefilename,
									tsubpath= targetsubpath, tfilename= targetfilename)	
		return resp


	@classmethod
	def convert_time_format(cls,strtime):
		return time.strftime(cls._output_time_format,time.strptime(strtime, cls._input_time_format))

	@classmethod
	def convert_fab_format(cls,fabcode):
		spcyxfabmap = ConfigLoader.config("spcyxfabmap")
		mfabcode = spcyxfabmap[fabcode]
		return mfabcode

	@classmethod
	def verify_run_mode(run_mode):
		pass

	@classmethod
	def verify_owner_code(owner_code):
		pass