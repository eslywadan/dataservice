from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
import requests


class IntRptConnect():
    _inttoken = ConfigLoader.config("source_ip")["int_token_server"][0]
    _intapi = ConfigLoader.config("source_ip")["int_api_server"][0]
    _identity = SecretLoader.secret("source_secret")

    def __init__(self):
        pass

    def get_apikey(self):
        url = '%s%s' % (self._inttoken, self._identity["int_token_server"][0])
        apikey = requests.get(url)
        return apikey
        
    def apikey(self):
        self.apikey = self.get_apikey
