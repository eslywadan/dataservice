from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
import requests


class IntRptConnect():
    _intrpt = ConfigLoader.config("source_ip")
    _identity = SecretLoader.secret("source_secret")

    def __init__(self):
        pass

    def get_api_key(self):
        url = '%s%s' % (self._intrpt["int_token_server"][0], self._identity["int_token_server"][0])
        res = requests.get(url)
        self.apikey = res
