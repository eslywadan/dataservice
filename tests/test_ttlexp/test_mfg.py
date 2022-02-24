import pytest
from ttlexp import create_app

api_token = ""

def test_get_token(test_client):
  headers = {'clientId': 'waterstat', 'password':'waterstat'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  assert api_token == '21ee8d77-98fa-303b-a52d-51ee5075aec0'

def test_product_qtime(test_client):
  url = '/ds/mfg/qtime/TFT5/TG5515BF7'
  headers = {'Content-Type': 'application/json', 'token': api_token}
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'


