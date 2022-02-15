from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_equal
import os
import sys
from ttlsap.adapter.intrpt import IntRptConnect

def test_ttlsap_adapter_intrpt():
    """test the intrpt under ../ttlsap/adapter by mocking the intrpt api token server """
    intrpt = IntRptConnect()
    assert intrpt._identity == {'int_token_server': ['eynenfgndsdfdfdfdwedfdwed']} 
    assert intrpt._inttoken == 'http://INTRPT/web/Verify.svc/API/'
    assert intrpt._intapi == 'http://intrpt/web/LinkPortal.ashx'

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


if __name__ == '__main__':
        print(sys.path)
        print(os.environ['PYTHON_PATH'])
        test_ttlsap_adapter_intrpt()
