import requests
import json


def get_token(apiserver,**kwargs):
    headers = {'clientId': kwargs['clientID'], 'password':kwargs['password']}
    url = "http://%s/api/Login" %apiserver
    r = requests.get(url, headers=headers)
    try:
        api_token = r.json()
    except:
        api_token = r.text
    return api_token 
    
def url_spec_mfg(apiserver,*args):
    tmp_url = 'http://%s/ds/mfg/%s/%s/products/%s'%(apiserver, args[0], args[1], args[2])
    url = tmp_url
    return url

def url_spec_eng(apiserver,*args, **kwargs):
    tmp_url = 'http://%s/ds/eng/%s/%s/%s/items/%s'%(apiserver,args[0], args[1], args[2], args[3])
    qstr = '?start_time=%s&end_time=%s&sub_equip=%s'%(kwargs['start_time'], kwargs['end_time'], kwargs['sub_equip'])
    url = tmp_url+qstr
    return url


def get_api(url,token):
    headers = {'Content-Type': 'application/json', 'apikey': token}
    response = requests.get(url, headers=headers)
    json_list = response.json()
    return json_list


if __name__ == '__main__':

    apiserver = 'hp08448w:8080'
    client = 'ds_test'
    password = 'ds_test'

    token =  get_token(apiserver,clientID=client,password=password)
    url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7')
    data = get_api(url, token)
    with open('qtime_TFT5_TG5515BF7.json','w') as f:
      json.dump(data, f)
    
    url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7,TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF')
    data = get_api(url, token)
    with open('qtime_TFT5_TG5515BF7&TGL320XKHAP&TG5515BF7A&TGL314BH&TGE505XFHSF.json','w') as f:
      json.dump(data, f)

    url = url_spec_eng(apiserver,'edcraw','TFT8','PFRW0100','AKCH_EXH_PRES',start_time='20220114140000',end_time='20220114160000',sub_equip='PFRW0100')
    data = get_api(url,token)
    with open('edcraw_TFT8_PFRW0100_AKCH_EXH_PRES.json','w') as f:
      json.dump(data, f)