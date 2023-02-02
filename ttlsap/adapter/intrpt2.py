from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
import requests
import json


class IntRptConnect2():
    """IntRptConnect2 is a brand new version compared to IntRptConnect."""
    _inttoken = ConfigLoader.config("source_ip")["int_token_server2"][0]
    _intapiservers = ConfigLoader.config("source_ip")["int_api_server2"]
    _identity = SecretLoader.secret("source_secret")
    clientid = None

    def __init__(self):
        pass

    def get_apikey(self,userid="PETER.PARK"):
        if self.clientid is not None: userid=self.clientid 
        url = '%s?user=%s&token=%s' % (self._inttoken, userid, self._identity["int_token_server2"][0])
        apikey = requests.get(url)
        if apikey.status_code == 200:
            self.apikey = apikey.text
        else:
            return       

    def filcrit_edcraw(self,**kwargs):
        """ accept the filter criteria for edc raw query and rearrange to a base64 encoded str ex:"fab=TFT_8_EDC&selQryType=T&FromDate=20210114140000&ToDate=20210114160000
        &txtIDList=&selMainEQP=PFRW0100&selSubEQP=PFRW0100&selEDCItem=AKCH_EXH_PRES" 
        The key word args ex: "fab='TFT_8_EDC',selQryType='T', FromDate='20210114140000', ToDate='20210114160000',
        , txtIDList='', selMainEQP='PFRW0100', selSubEQP='PFRW0100', selEDCItem='AKCH_EXH_PRES' "
        """
        fab = kwargs['fab']
        self._whichapiserver(fab)

        fstr_dict = {"fab":fab, "selQryType":kwargs['selQryType'], "FromDate": kwargs['FromDate'], "ToDate": kwargs['ToDate'],
                    "txtIDList": kwargs['txtIDList'], "selMainEQP": kwargs['selMainEQP'], "selSubEQP":kwargs['selSubEQP'], 
                    "selEDCItem":kwargs['selEDCItem'], "txtOper":"", "txtProd":""}
        self.clientid = kwargs['clientid']
        self.param = fstr_dict

    def _whichapiserver(self,fab):
        """
            "TFTT6":"TFT_L_EDC","CFT6":"CF_L_EDC","LCDT6":"LCD_L_EDC" will use the different API server
        """
        self._intapi = self._intapiservers[0]
        if fab.split("_")[1] == "L":
            self._intapi = self._intapiservers[1]

    def set_linkpage(self,funname="EDC_NET_CF"):
        """ the fun accept the funname such as "EDC_RAW" and find the link page (read the int source api defined in config)
        then encode the link page into base64
        """
        print(ConfigLoader.config("int_source_api")[funname])
        if ConfigLoader.config("int_source_api")[funname] is not None:
            self.linkpage = ConfigLoader.config("int_source_api")[funname][0]

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
        linkpage = self.linkpage
        ticketKey = self.apikey

        self.qurl = "%s%s?linksrc=API" %(apiserver, linkpage)
        response = requests.post(self.qurl,json=self.param ,headers={"Authorization": "Bearer " + ticketKey, "Content-Type": "application/json; charset=utf-8"})
        if response.status_code == 200:
            if (response.json()['status'] == 'error') and (response.json()['message'] == '@{expired}'):
                self.reqret_code = '401'
            else:
                self.reqret_code = '200'
        else:
            self.reqret_code = '500'

        self.resp = response
    