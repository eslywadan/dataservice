from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none
from ttlsap.adapter.intrpt import IntRptConnect


@patch('ttlsap.adapter.intrpt.requests.get')
def test_ttlsap_adapter_intrpt(mock_get):
    """test the intrpt under ../ttlsap/adapter by mocking the intrpt api token server """
    mock_get.return_value.ok = True
    
    print("test the get api key from intrpt toekn server")
    
    intrpt = IntRptConnect()
    assert intrpt._identity == {'int_token_server': ['eynenfgndsdfdfdfdwedfdwed']} 
    assert intrpt._intrpt == {'int_api_server': ['http://intrpt/web/LinkPortal.ashx'], 'int_token_server': ['http://INTRPT/web/Verify.svc/API/']}
    intrpt.get_api_key()
    assert_is_not_none(intrpt.apikey)
    
