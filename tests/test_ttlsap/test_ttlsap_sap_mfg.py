from os import curdir
from unittest.mock import  Mock, patch
from nose.tools import assert_is_none, assert_equal
from ttlsap.sa_mfg import MfgApi
from tools.config_loader import ConfigLoader
from tools.mock_data import *
from pathlib import Path
import json


mock_level = ConfigLoader.config("test_env")["mock_level"][0]

def test_ttlsap_sa_mfg():
    """ test the source adapter of MFG api server by mocking function if te mock_level == 1 or test the 
        unit function interacting with  the MFG API server
    """
    mfgapis = MfgApi()
    apiserver = "http://zipsum/MFGReport"
    assert_equal(mfgapis.apiserver, apiserver)

    
    if mock_level == 1:
        mock_dat = get_mock_data(file_name="sample")
        with patch('ttlsap.sa_mfg.requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = mock_dat
            response = mfgapis.web_api(apiserver)
            
    test_fab = "TFT5"
    test_product = "TGE505XFHSF"


    req_data = mfgapis.productqtime(test_fab,test_product)
    assert_equal(mfgapis.response.status_code, 200)

    curdir = Path.cwd()
    data_path = '%s/data/mfg_test_data' % curdir
    mfg_test_data = Path(data_path)
    print(curdir, mfg_test_data)
    productqtime_data_path = mfg_test_data / "source_api_product_qtime.json"
    if productqtime_data_path.exists():
        last_file = json.load(productqtime_data_path.open())
        # assert_equal(last_file, req_data)

    mfg_test_data.mkdir(exist_ok=True)
    productqtime_data_path.write_text(json.dumps(req_data))


    req_data = mfgapis.productroute(test_fab,test_product)
    assert_equal(mfgapis.response.status_code, 200)

    productroute_data_path = mfg_test_data / "source_api_product_route.json"
    #if productroute_data_path.exists():
    #    last_file = json.load(productroute_data_path.open())
    #    assert_equal(last_file, req_data)

    mfg_test_data.mkdir(exist_ok=True)
    productroute_data_path.write_text(json.dumps(req_data))

    
    req_data = mfgapis.productrecipe(test_fab,test_product)
    assert_equal(mfgapis.response.status_code, 200)


    #productrecipe_data_path = mfg_test_data / "source_api_product_recipe.json"
    #if productrecipe_data_path.exists():
    #    last_file = json.load(productrecipe_data_path.open())
    #    assert_equal(last_file, req_data)

    # mfg_test_data.mkdir(exist_ok=True)
    # productrecipe_data_path.write_text(json.dumps(req_data))

    


