import pytest


def test_portal(test_client):
  response = test_client.get('/')
  assert response.status_code == 200
  response = test_client.get('/home')
  assert response.status_code == 200

def test_get_token(test_client):
  headers = {'clientId': 'waterstat', 'password':'waterstat'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  assert api_token == '21ee8d77-98fa-303b-a52d-51ee5075aec0'
