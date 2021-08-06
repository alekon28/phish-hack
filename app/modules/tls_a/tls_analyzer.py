import ssl
import requests
from requests.exceptions import SSLError


class SearchAnalyzer(object):
    def __init__(self, link: str):
        self.link = link

    def verify_tls(self):
        try:
            r = requests.get(self.link, verify=True)
        except SSLError as e:
            return False
        else:
            return True