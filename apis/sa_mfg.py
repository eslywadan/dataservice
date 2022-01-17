import requests
import pandas as pd
import json


class MfgApi():
    apiserver = 'http://TNVTMFGRPT01/MFGWebAPI'

    def __init__(self):
        pass

    @staticmethod
    def web_api(url):
        response = requests.get(url)
        json_list = response.json()
        return json_list

    @classmethod
    def url_getproductqtime(cls, FAB_ID, PROD_ID):
        url = '%s/api/Home/GetProductQTime?fac=%s&prod=%s' % (cls.apiserver, FAB_ID, PROD_ID)
        return url

    def productqtime(self, FAB_ID, PROD_ID):
        url = self.url_getproductqtime(FAB_ID, PROD_ID)
        data = self.web_api(url)
        return data
