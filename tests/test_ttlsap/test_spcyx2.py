from ttlsap.adapter.spcyx2 import SpcYx, get_spcyx_data
from tests.auxinfo import SpcYxInfo

def test_SpcYx2():

	""" info dict
	info = {"fab":fab,"chart_list":chart_list,"token":token,"start_dttm":start_dttm,"end_dttm":end_dttm,"method":method,
	"product":product, "pproc_id":pproc_id,"peqpt_id":peqpt_id,"precipe_id":precipe_id,"owner_code":owner_code,
	"run_mode":run_mode,"spc_item_id":spc_item_id,"proc_id":proc_id}"""

	spcyxinfo = SpcYxInfo()
	spcyx = SpcYx(spcyxinfo._info)

	spcyx.get_spc_data()
	assert len(spcyx.spc_data) == 22

	spcyx.get_item_list(restrict_op=False)
	assert len(spcyx.item_list) == 580

	spcyx.get_eqpt_list()
	assert len(spcyx.eqpt_list) == 1

	spcyx.get_edc_data()
	assert len(spcyx.edc_data_raw) == 36

	spcyx.wrangle_edc_data()
	assert len(spcyx.edc_data_raw.columns) == 596
	assert len(spcyx.edc_data_c1.columns) == 589

	spcyx.merge_spc_edc_data()

	"""integration test"""
	resp = get_spcyx_data(spcyxinfo._info,"test_spcyx")
	assert resp["status"] == 200


