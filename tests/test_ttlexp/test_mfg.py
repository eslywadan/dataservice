def test_get_token(test_client):
  headers = {'clientId': 'mfg', 'password':'mfg'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  return api_token 

def test_products_qtime_recipe_route_get(test_client):
  account_token = test_get_token(test_client)
  headers = {'Content-Type': 'application/json', 'apikey': account_token}
  prod_list = '/TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF'
  
  prefix_url = '/ds/mfg/qtime/TFT5/products'
  url = '%s%s'%(prefix_url, prod_list)
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK' 

  prefix_url = '/ds/mfg/recipe/TFT5/products'
  url = '%s%s'%(prefix_url, prod_list)
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'
  assert r.json is not None

  prefix_url = '/ds/mfg/route/TFT5/products'
  url = '%s%s'%(prefix_url, prod_list)
  r = test_client.get(url, headers=headers)
  assert r.status == '200 OK'
  assert r.json is not None

def test_wrong_token(test_client):
  headers = {'clientId': 'eng', 'password':'eng'}
  response = test_client.get('/api/Login', headers=headers)
  api_token = response.json
  prefix_url = '/ds/mfg/recipe/TFT5/products'
  prod_list = '/TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF'
  headers = {'Content-Type': 'application/json', 'apikey': api_token}
  url = '%s%s'%(prefix_url, prod_list)
  r = test_client.get(url, headers=headers)
  assert r.status == '403 FORBIDDEN'
