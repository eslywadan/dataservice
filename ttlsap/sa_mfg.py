import requests
import json
from tools.config_loader import ConfigLoader


class MfgApi():
    apiserver = ConfigLoader.config("source_ip")["mfg_api_server"][0]
    mfgapi = ConfigLoader.config("mfg_source_api")

    def __init__(self):
        pass

    def web_api(self, url, FAB_ID, PROD_ID):
        payload = {"Shop": FAB_ID, "Prod": PROD_ID}
        self.response = requests.post(url, data=payload)
        return self.response.json()

    @classmethod
    def url_getproductapi(cls, FUNC):
        url = '%s%s' % (cls.apiserver, cls.mfgapi[FUNC][0])
        return url

    def productqtime(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi("prod_qtime")
        return self.web_api(url, FAB_ID, PROD_ID)

    def productrecipe(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi( "prod_recipe" )
        return self.web_api(url, FAB_ID, PROD_ID)

    def productroute(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi( "prod_route")
        return self.web_api(url, FAB_ID, PROD_ID)

