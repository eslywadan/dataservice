import pytest
from tools.crypto import *
import tools.request_handler as req


def test_portal(test_client):
  response = test_client.get('/')
  assert response.status_code == 200
  response = test_client.get('/home')
  assert response.status_code == 200

def test_get_token(test_client):
  headers = {'clientId': 'waterstat', 'password':'waterstat'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  assert api_token == get_account_token('waterstat')

def test_check_and_log_fail(test_client):
  wrong_api_token = '12345'
  headers = {'Content-Type': 'application/json', 'token': wrong_api_token}
  res = test_client.get('/ds/mfg/TFT5/TG5515BF7',headers=headers)
  assert res.status == '404 NOT FOUND'


