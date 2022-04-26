import requests
import json
from tools.config_loader import ConfigLoader


class MfgApi():
    apiserver = ConfigLoader.config("source_ip")["mfg_api_server"][0]
    mfgapi = ConfigLoader.config("mfg_source_api")

    def __init__(self):
        pass

    def web_api(self, url):
        self.response = requests.get(url)
        return self.response.json()

    @classmethod
    def url_getproductapi(cls, FAB_ID, PROD_ID, FUNC):
        url = '%s%s?fac=%s&prod=%s' % (cls.apiserver, cls.mfgapi[FUNC][0], FAB_ID, PROD_ID)
        return url

    def productqtime(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi(FAB_ID, PROD_ID, "prod_qtime")
        return self.web_api(url)

    def productrecipe(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi(FAB_ID, PROD_ID, "prod_recipe" )
        return self.web_api(url)

    def productroute(self, FAB_ID, PROD_ID):
        url = self.url_getproductapi(FAB_ID, PROD_ID, "prod_route")
        return self.web_api(url)

