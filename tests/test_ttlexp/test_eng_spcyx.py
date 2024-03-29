from tests.auxinfo import SpcYxInfo

def test_get_token(test_client,client_id="eng",password="eng"):
  headers = {'clientId': client_id, 'password':password}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  return api_token


def test_spcyx_data(test_client,client_id="eng",password="eng"):
  """http://host:port/ds/eng/spcyx/TFT7/438N/MB_X/TJDF40XK/DF40XK_A5_4_254A/4300
     ?start_time=20220712080000&end_time=20220712170000&run_mode=N&owner_code=CRN0&peqpt=TLCD0300
     &token=account_token"""
  case = SpcYxInfo('spcyx1')
  account_token = test_get_token(test_client,client_id, password)
  named_data = case.named_data
  qstr = case.qstr
  nowait = "&nowait=false"
  url = '%s%s%s'%(named_data, qstr, nowait)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

def test_spcyx_data_nowait(test_client,client_id="eng",password="eng"):
  """http://host:port/ds/eng/spcyx/TFT7/438N/MB_X/TJDF40XK/DF40XK_A5_4_254A/4300
     ?start_time=20220712080000&end_time=20220712170000&run_mode=N&owner_code=CRN0&peqpt=TLCD0300
     &token=account_token"""
  account_token = test_get_token(test_client,client_id, password)
  case = SpcYxInfo('spcyx2')
  account_token = test_get_token(test_client,client_id, password)
  named_data = case.named_data
  qstr = case.qstr
  nowait = "&nowait=true"
  url = '%s%s%s'%(named_data, qstr, nowait)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'  