from tests.test_ttlexp.conftest import test_client


def test_get_apikey_arg(test_client):
  response = test_client.get('/ds/utility/apikey/?clientId=mfg&password=mfg')
  apikey = response.json
  assert response.status == '200 OK'

  response = test_client.get('/ds/utility/apikey/?clientid=mfg&password=mfg')
  apikey = response.json
  assert response.status == '401 UNAUTHORIZED'

def test_get_token(test_client):
  headers = {'clientId': 'mfg', 'password':'mfg'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  assert response.status == '200 OK'
  return api_token