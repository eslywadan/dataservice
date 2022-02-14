from unittest.mock import  Mock, patch
from nose.tools import assert_is_none, assert_equal
from ttlsap.sa_mfg import MfgApi
from tools.mock_data import *

def test_ttlsap_sa_mfg():
    """ test the source adapter of MFG api server by mocking function """
    mfgapis = MfgApi()
    apiserver = "http://TNVTMFGRPT01/MFGWebAPI"
    assert_equal(mfgapis.apiserver, apiserver)

    # mock_dat = get_mock_data(file_name="productqtime")
    mock_dat = get_mock_data(file_name="sample")
    with patch('ttlsap.sa_mfg.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_dat
        response = mfgapis.web_api(apiserver)
        
    assert_equal(response, mock_dat)
    

@patch('ttlsap.sa_mfg.MfgApi.productqtime')