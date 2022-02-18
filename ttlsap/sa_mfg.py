import requests
import json
from tools.config_loader import ConfigLoader


class MfgApi():
    apiserver = ConfigLoader.config("source_ip")["mfg_api_server"][0]

    def __init__(self):
        pass

    def web_api(self, url):
        self.response = requests.get(url)
        return self.response.json()

    @classmethod
    def url_getproductqtime(cls, FAB_ID, PROD_ID):
        url = '%s/api/Home/GetProductQtime?fac=%s&prod=%s' % (cls.apiserver, FAB_ID, PROD_ID)
        return url

    def productqtime(self, FAB_ID, PROD_ID):
        url = self.url_getproductqtime(FAB_ID, PROD_ID)
        return self.web_api(url)
