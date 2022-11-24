from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_equal
from tools.config_loader import ConfigLoader
from ttlsap.adapter.intrpt import IntRptConnect
from ttlsap.sa_eng import EdcRawApi
from pathlib import Path
import json

mock_level = ConfigLoader.config("test_env")["mock_level"][0]

def test_ttlsap_adapter_intrpt():
	"""test the intrpt under ../ttlsap/adapter by mocking the intrpt api token server if mock_level == 1
		, or test the unit interact with the int token server and api server.
	 """
	intrpt = IntRptConnect()
	assert intrpt._inttoken == 'http://INTRPT/web/Verify.svc/API/'

	if mock_level == 1:
		print("Tests using the mock function")
		assert intrpt._identity == {'int_token_server': ['eynenfgndsdfdfdfdwedfdwed']} 
		mock_api_key = [{'apikey':"erutn545"}]
		with patch('ttlsap.adapter.intrpt.requests.get') as mock_get:
			mock_get.return_value.ok = True
			mock_get.return_value.json.return_value = mock_api_key
			res = intrpt.get_apikey()
			print(res)
		assert res.json()[0] ==  mock_api_key[0]

		with patch('ttlsap.adapter.intrpt.requests.get') as mock_get:
			mock_get.return_value.ok = False
			mock_get.return_value.json.return_value = None
			res = intrpt.get_apikey()
		assert_is_none(res.json())
	
	else:
		intrpt.get_apikey()
  
	from_date = "20220114140000"
	to_date = "20220114160000"
	intrpt.filcrit_edcraw(fab="TFT_8_EDC",selQryType="T",FromDate=from_date,ToDate=to_date,txtIDList="",selMainEQP="PFRW0100",selSubEQP="PFRW0100",selEDCItem="AKCH_EXH_PRES")
	
	filter_args_in_dic = {"fab":"TFT_8_EDC","selQryType":"T","FromDate":from_date,"ToDate":to_date,"txtIDList":"","selMainEQP":"PFRW0100","selSubEQP":"PFRW0100","selEDCItem":"AKCH_EXH_PRES"}
	intrpt.filcrit_edcraw(**filter_args_in_dic)
	
	funname = "EDC_RAW_TFT"
	link_page = "/WEB/WAPI/EDC/EDC_TFT_EDCQuery_API.ashx"
	intrpt.linkpage(funname)
	
	assert intrpt._intapi == 'http://intrpt/web/LinkPortal.ashx'
	assert intrpt.linkpage == link_page
	assert intrpt.linkpageencode == b"L1dFQi9XQVBJL0VEQy9FRENfVEZUX0VEQ1F1ZXJ5X0FQSS5hc2h4"
	
	
	qry_res = intrpt.request_api()
	print(intrpt.resp.url)
	print(intrpt.resp.status_code)
	assert intrpt.reqret_code == '200'

	curdir = Path.cwd()
	data_path = '%s/data/eng_test_data' % (curdir)
	eng_test_data = Path(data_path)
	edc_raw_data_path = eng_test_data / "source_api_edc_raw.json"
	assert len(intrpt.resp.json()) > 0
	if edc_raw_data_path.exists():
		last_file = json.load(edc_raw_data_path.open())
		assert len(last_file) == len(intrpt.resp.json())

	eng_test_data.mkdir(exist_ok=True)
	edc_raw_data_path.write_text(json.dumps(intrpt.resp.json()))

	edcrawapi = EdcRawApi()
	data = edcrawapi.edcrawbytime(fab="TFT8",equip="PFRW0100",edc="AKCH_EXH_PRES",start_time=from_date,
            end_time=to_date,sub_eq="PFRW0100",grp_id="")
	
	assert edcrawapi.linkpageencode == intrpt.linkpageencode
	assert edcrawapi.filter == intrpt.filter
	assert edcrawapi.filterencode == intrpt.filterencode
	#assert edcrawapi.apikey == intrpt.apikey
	#assert edcrawapi.linkkey == intrpt.linkkey
	
	print(f"edcrawapi:{edcrawapi.url}")
	#assert edcrawapi.url == intrpt.url
	print(f"intrpt:{intrpt.url}")
	assert data == intrpt.resp.json()
	