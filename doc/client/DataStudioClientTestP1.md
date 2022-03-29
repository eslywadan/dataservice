# Data Studio Client Test (於INX Cloud 雲平台上測試)
## 測試情境
使用者已有 Client ID 與　Password , 透過 Data Studio 獲取 API key, 並以之取用 Data Service 的服務。

### Testing Script 1 - via Swagger UI 
1. 取得 API Key
    - 將以下 url http://10.55.8.214:15943/ds/utility/ 貼到瀏覽器列進行測試
    - 點擊 'defaul' 會看到展開頁 'GET /apikey/'。
    - 點擊 'Try it out' icon, 依序輸入 client id 以及 password 。
    - 點擊 'execute' icon, 確認 return code 為 '200' 以及 apikey 出現在 response body. 可以點擊 'Downlod' 或 'copy' icon 以取得 apikey.
2. 取得 'Q time' data
    - 將以下 url http://10.55.8.214:15943/ds/mfg 貼到瀏覽器列進行測試
    - 點擊 'defaul' 會看到展開頁 'GET /qtime/{fab}/products/{list_products}' 。
    -  點擊 'Try it out' icon, 在 'token'欄位輸入在上一個步驟取得之 apikey。
    -  在 fab 輸入 'TFT5' 以及在 products 輸入單一產品料號 'TG5515BF7' 亦可多個料號 'TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF' 然後按 'Execute'.
    -  請注意輸入時要去掉單引號 ''。
    -  預期看到 return code 200 以及 qtime data 出現在 response body。
    -  可以點擊 'Downlod' 或 'copy' icon 以取得 data。



### Testing Script 2 - Python client
1. 如果尚未安裝　Python，可以到以下網站 https://www.python.org/downloads/ 下載並安裝。
2. 複製以下代碼並在本機存成 'ds_python_client.py' 
3. 修改 client id 以及 password 
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

    apiserver = '10.55.8.214:15943'
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

```

4. 打開 windows command 或 powersehll 進入 python 模式
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
5. 在 Python 模式下輸入 "from ds_python_client import *" 並依序輸入以下代碼執行
``` language=python
>>>　from ds_python_client import *
>>>  apiserver = '10.55.8.214:15943'
>>>  client = 'your registed client id'
>>>  password = 'your registed client password'

>>>  token =  get_token(apiserver,clientID=client,password=password)
     url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7')
     data = get_api(url, token)
     with open('qtime_TFT5_TG5515BF7.json','w') as f:
        json.dump(data, f)

>>> url = url_spec_mfg(apiserver,'qtime','TFT5', 'TG5515BF7,TGL320XKHAP,TG5515BF7A,TGL314BH,TGE505XFHSF')
  data = get_api(url, token)
  with open('qtime_TFT5_TG5515BF7&TGL320XKHAP&TG5515BF7A&TGL314BH&TGE505XFHSF.json','w') as f:
    json.dump(data, f)


```
6. 亦可以在 command window 或 powershell window 直接執行檔案. 預期會有 2 個檔案產生。
```language=powershell
PS D:\projects\dsclient\test> python ds_python_client.py
PS D:\projects\dsclient\test> ls


    目錄: D:\projects\dsclient\test


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----      2022/3/15  下午 04:05           1839 ds_python_client.py
-a----      2022/3/15  下午 04:14          11846 qtime_TFT5_TG5515BF7&TGL320XKHAP&TG5515BF7A&TGL314BH&TGE505XFHSF.json
-a----      2022/3/15  下午 04:14           1577 qtime_TFT5_TG5515BF7.json
```


###### tags: `Data Studio`