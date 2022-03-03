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

def test_product_qtime(test_client):
  url = '/ds/mfg/qtime/TFT5/TG5515BF7'
  headers = {'Content-Type': 'application/json', 'token': account_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'

def test_products_qtime(test_client):
  url = '/ds/mfg/qtime/TFT5/products'
  headers = {'Content-Type': 'application/json', 'token': account_token}
  prod_list = ['TGL320XKHAP','TG5515BF7A','TGL314BH','TGE505XFHSF']
  payload = {"prod_list": prod_list}
  data = json.dumps(payload)
  r = test_client.post(url, headers=headers, data=data)
  assert r.status == '200 OK'


