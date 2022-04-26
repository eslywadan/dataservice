def test_get_token(test_client):
  headers = {'clientId': 'waterstat', 'password':'waterstat'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  return api_token

def test_edc_data(test_client):
  account_token = test_get_token(test_client)
  named_data = '/ds/eng/edcraw/TFT8/PFRW0100/items/AKCH_EXH_PRES'
  qstr = '?subEQP=PFRW0100&FromDate=20210114140000,ToDate=20210114160000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

  named_data = '/ds/eng/edcraw/TFT8/PFRW0100/items/AKCH_EXH_PRES,AKCH_EXH_PRES'
  qstr = '?subEQP=PFRW0100&FromDate=20210114140000,ToDate=20210114160000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

  named_data = '/ds/eng/edcraw/TFT2/CVDA0100/items/E_VALVE_1   E_VALVE_1AVGS'
  qstr = '?subEQP=CVDA0100&FromDate=20210114140000,ToDate=20220406000000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

  named_data = '/ds/eng/edcraw/TFTT6/CVDA0100/items/1GAS1'
  qstr = '?subEQP=CVDA0100&FromDate=20220401000000,ToDate=20220401000000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

  named_data = '/ds/eng/edcraw/CFT6/CNVR0500/items/Process_Ttime'
  qstr = '?subEQP=CNVR0500&FromDate=20220401070000,ToDate=20220402070000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

  named_data = '/ds/eng/edcraw/LCDT6/PIPR0500/items/Total_Tact_Time'
  qstr = '?subEQP=PIPR0506&FromDate=20220325000000,ToDate=20220405000000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'


