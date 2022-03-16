# Data Studio Client Test
## Testing Scenario
A client user would like to get the data via data service's api with an secure api key. The scenario begins with prerequist for client registering,  and then a touring throgh swagger UI, finalized requesting the data service by Python's client.
## Prerequist
The client must have a reistered account. If you have not the account, please visit http://hp08448w:3400 and create one for yourself.
The user id have used for opening the account mangement system will be the default owner of the client. An owner can create one to several clients. The client id and password you haved registered will be used for granting an apikey latter. 
The query previledge is enabled by default. Please contact the admin once you have not the access previledge after you have created the account. (admin contact:)
### Testing Script - via Swagger UI 
1. Get the api key
    - place the url http://hp08448w:8080/ds/utility at your browser
    - Click on the 'defaul' and the expand page will show the 'GET /apikey/' in a RESTful style.
    - Click on the 'Try it out' icon located at the upper right corner, then it will be allowed to enter the client id and password that you have created in the prerequist.
    - Click on the execute, then check the return code is '200' and the apikey is in the response body. You could click 'Downlod' or 'copy' icon to get the apikey.
2. Get 'Q time' data
    - Place the url http://hp08448w:8080/ds/mfg at your browser
    - Also a clean page with API text at the upper left corner. Expand the page by clickng the arrow down symbol. The page will show 'GET /qtime/{fab}/products/{list_products}' in a RESTful style.
    -  Click on the 'Try it out' icon, then it will be allowed to enter the 'token' that is the apikey you have got in the step 1.
    -  Enter the fab 'TFT5' and products for single 'TG5515BF7' or multiple 'TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF' and press 'Execute'.
    -  Please note that the '' symbol is not required whenever you past the token or fab, products etc.
    -  You are expected to see the return code 200 and the requesed qtime data in the response body.
    -  Also you could copy or download the data.
3. Get 'EDC' data
    - Place the url http://hp08448w:8080/ds/eng at your browser
    - likewise the step 2, expand the page and you will see the 'GET / edcraw/{fab}/{equip}/items/{item_list}'
    - Click on the 'Try it out', enter the parameters in a sequence manner
        - start_time: 20220114140000
        - end_time: 20220114160000
        - sub_equip: PFRW0100
        - token: XXXX
        - fab: TFT8
        - equip: PFRW0100
        - item_list: AKCH_EXH_PRES
    - You are expexted to get the return code 200 and the requested edc data in the response body.


### Testing Script - Python client
1. You are assumed have the python installed in your desktop. If not yet, visit the https://www.python.org/downloads/ and install it.
2. Copy below code and save as a python file such as 'ds_python_client.py' in your local disk.
``` langualge=python
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
    client = 'your client'
    password = 'password of your client'

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
```

4. open a command window or a powersehll window, go to the directory you have save above file, and type 'python' to enter the python mode.
```language=powershell
PS D:\projects\dsclient> ls ds_python_client.py


    目錄: D:\projects\dsclient


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----      2022/3/15  下午 04:00           1875 ds_python_client.py


(flask) PS D:\projects\dsclient> python 
Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
5. Type "from ds_python_client import *" and execute below code in a sequence manner
``` language=python
>>>　from ds_python_client import *
>>>  apiserver = 'hp08448w:8080'
>>>  client = 'ds_test'
>>>  password = 'ds_test'

>>>  token =  get_token(apiserver,clientID=client,password=password)
     url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7')
     data = get_api(url, token)
     with open('qtime_TFT5_TG5515BF7.json','w') as f:
        json.dump(data, f)

>>> url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7,TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF')
  data = get_api(url, token)
  with open('qtime_TFT5_TG5515BF7&TGL320XKHAP&TG5515BF7A&TGL314BH&TGE505XFHSF.json','w') as f:
    json.dump(data, f)

>>>  url = url_spec_eng(apiserver,'edcraw','TFT8','PFRW0100','AKCH_EXH_PRES',start_time='20220114140000',end_time='20220114160000',sub_equip='PFRW0100')
  data = get_api(url,token)
  with open('edcraw_TFT8_PFRW0100_AKCH_EXH_PRES.json','w') as f:
    json.dump(data, f)
```
6. You can also execute the python file directly on the command window or powershell window. There would be 3 files generated as expexted.
```language=powershell
PS D:\projects\dsclient\test> python ds_python_client.py
PS D:\projects\dsclient\test> ls


    目錄: D:\projects\dsclient\test


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----      2022/3/15  下午 04:05           1839 ds_python_client.py
-a----      2022/3/15  下午 04:14          12691 edcraw_TFT8_PFRW0100_AKCH_EXH_PRES.json
-a----      2022/3/15  下午 04:14          11846 qtime_TFT5_TG5515BF7&TGL320XKHAP&TG5515BF7A&TGL314BH&TGE505XFHSF.json
-a----      2022/3/15  下午 04:14           1577 qtime_TFT5_TG5515BF7.json
```


###### tags: `Data Studio`