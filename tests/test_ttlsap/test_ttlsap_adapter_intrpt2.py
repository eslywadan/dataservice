from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_equal
from tools.config_loader import ConfigLoader
from ttlsap.adapter.intrpt2 import IntRptConnect2
from ttlsap.sa_eng import EdcRawApi
from pathlib import Path
import json

def test_ttlsap_adapter_intrpt2():
	"""test the intrpt under ../ttlsap/adapter by mocking the intrpt api token server if mock_level == 1
		, or test the unit interact with the int token server and api server.
	 """
	intrpt = IntRptConnect2()
	assert intrpt._inttoken == "http://intrpt/net/Verify/API_CENTER"

  
	from_date = "20221114080000"
	to_date = "20221114090000"
	intrpt.filcrit_edcraw(fab="CF_6_EDC",selQryType="T",FromDate=from_date,ToDate=to_date,txtIDList="",selMainEQP="CNVR0400",selSubEQP="CNVR0411",selEDCItem="Glass_ ID",clientid="PETER.PARKER")
	
	funname = "EDC_NET_CF"
	intrpt.set_linkpage(funname)
	intrpt.get_apikey()
	
	assert intrpt._intapi == "http://intrpt/net/Dynamic/DATAMODEL"
	
	qry_res = intrpt.request_api()
	print(intrpt.resp.url)
	print(intrpt.resp.status_code)
	assert intrpt.reqret_code == '200'

	edcrawapi = EdcRawApi()
	data = edcrawapi.edcnetbytime(fab="CF6",equip="CNVR0400",edc="Glass_ ID",start_time=from_date,
            end_time=to_date,sub_eq="CNVR0411",grp_id="",clientid="PETER.PARKER")
	

	assert data == intrpt.resp.json()
	