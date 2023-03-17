from ttlsap.adapter.spcyx2 import SpcYx, get_spcyx_data
from tests.auxinfo import SpcYxInfo
import os

def test_SpcYx2():

	""" info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""

	casefilepath = os.path.join('tests/doc/testcases', 'spcyx-testcases.json')
	spcyxinfo = SpcYxInfo(casefilepath,'spcyx1')
	spcyx = SpcYx(spcyxinfo._info)

	spcyx.gen_sql_get_spc_data()

	spcyx._sql_get_spc_data

	spcyx.get_spc_data()
	assert spcyx.spc_data is not None

	spcyxinfo = SpcYxInfo(casefilepath,'spcyx2')
	spcyx2 = SpcYx(spcyxinfo._info)
	spcyx2.gen_sql_get_spc_data()

	spcyx2._sql_get_spc_data

	spcyx2.get_spc_data()
	assert spcyx2.spc_data is not None
	
	spcyx.get_item_list(restrict_op=False)
	assert spcyx.item_list is not None

	spcyx.get_eqpt_list()
	assert spcyx.eqpt_list is not None

	spcyx.get_edc_data()
	assert spcyx.edc_data_raw is not None

	spcyx.wrangle_edc_data()
	assert spcyx.edc_data_raw.columns is not None
	assert spcyx.edc_data_c1.columns is not None

	spcyx.merge_spc_edc_data()

	"""integration test"""
	resp = get_spcyx_data(spcyxinfo._info,"test_spcyx")
	assert resp["status"] == 200


