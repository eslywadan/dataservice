from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
import requests
import base64


class IntRptConnect():
    _inttoken = ConfigLoader.config("source_ip")["int_token_server"][0]
    _intapiservers = ConfigLoader.config("source_ip")["int_api_server"]
    _identity = SecretLoader.secret("source_secret")

    def __init__(self):
        self.get_apikey()

    def get_apikey(self):
        url = '%s%s' % (self._inttoken, self._identity["int_token_server"][0])
        apikey = requests.get(url)

        self.apikey = apikey        

    def filcrit_edcraw(self,**kwargs):
        """ accept the filter criteria for edc raw query and rearrange to a base64 encoded str ex:"fab=TFT_8_EDC&selQryType=T&FromDate=20210114140000&ToDate=20210114160000
        &txtIDList=&selMainEQP=PFRW0100&selSubEQP=PFRW0100&selEDCItem=AKCH_EXH_PRES" 
        The key word args ex: "fab='TFT_8_EDC',selQryType='T', FromDate='20210114140000', ToDate='20210114160000',
        , txtIDList='', selMainEQP='PFRW0100', selSubEQP='PFRW0100', selEDCItem='AKCH_EXH_PRES' "
        """
        fab = kwargs['fab']
        self._whichapiserver(fab)

        fstr = "fab=%s&selQryType=%s&FromDate=%s&ToDate=%s&txtIDList=%s&selMainEQP=%s&selSubEQP=%s&selEDCItem=%s" %(fab, kwargs['selQryType'], kwargs['FromDate'], kwargs['ToDate'], kwargs['txtIDList'], kwargs['selMainEQP'], kwargs['selSubEQP'], kwargs['selEDCItem'])
        fstr_base64en = base64.b64encode(fstr.encode('ascii'))
        
        self.filter = fstr
        self.filterencode = fstr_base64en

    def _whichapiserver(self,fab):
        self._intapi = self._intapiservers[0]
        if fab.split("_")[1] == "L":
            self._intapi = self._intapiservers[1]

    def linkpage(self,funname):
        """ the fun accept the funname such as "EDC_RAW" and find the link page (read the int source api defined in config)
        then encode the link page into base64
        """
        print(ConfigLoader.config("int_source_api")[funname])
        if ConfigLoader.config("int_source_api")[funname] is not None:
            self.linkpage = ConfigLoader.config("int_source_api")[funname][0]
            self.linkpageencode = base64.b64encode(self.linkpage.encode('ascii'))

    def request_api(self):
        """ requst return code:
            "100": Continue (Start and continue)
            "200": OK
            "401": Unauthorized
            "500": Internal Server Error
        """
        req_max_retry = int(ConfigLoader.config("source_api_config")["req_max_retry"][0])
        self.reqretry = 0
        self.resp_status = 100
        self.reqret_code = '9'
        while self.reqret_code != '200' and self.reqretry < req_max_retry:
            if self.reqret_code == '401'  :
                self.get_apikey()
            
            self._get_api()
            self.reqretry += 1

        return self.resp.json()

    def _get_api(self):
        apiserver = self._intapi
        linkpage = self.linkpageencode.decode('utf-8')
        linkin = self.filterencode.decode('utf-8')
        linkkey = self.apikey.content.decode('utf-8')
        self.linkkey = linkkey

        self.url = "%s?linkpage=%s&linklevel=0&linkin=%s&linkkey=%s" %(apiserver,linkpage,linkin,linkkey)
        response = requests.get(self.url)
        if response.status_code == 200:
            if (response.json()['status'] == 'error') and (response.json()['message'] == '@{expired}'):
                self.reqret_code = '401'
            else:
                self.reqret_code = '200'
        else:
            self.reqret_code = '500'

        self.resp = response
    