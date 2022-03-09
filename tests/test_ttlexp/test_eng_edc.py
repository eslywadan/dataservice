import pytest
import json
from ttlexp import create_app
from tools.crypto import *


account_token = get_account_token('waterstat')

def test_get_token(test_client):
  headers = {'clientId': 'waterstat', 'password':'waterstat'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  assert api_token == account_token

def test_edc_data(test_client):
  named_data = '/ds/eng/edcraw/TFT8/PFRW0100/items/AKCH_EXH_PRES'
  qstr = '?subEQP=PFRW0100&FromDate=20210114140000,ToDate=20210114160000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'token': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

def test_edc_data_muti_items(test_client):
  named_data = '/ds/eng/edcraw/TFT8/PFRW0100/items/AKCH_EXH_PRES'
  qstr = '?subEQP=PFRW0100&FromDate=20210114140000,ToDate=20210114160000'
  url = '%s%s'%(named_data, qstr)
  headers = {'Content-Type': 'application/json', 'token': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'
