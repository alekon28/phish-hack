from googlesearch import search
from urllib.parse import urlparse


class SearchAnalyzer(object):
    def __init__(self, domain: str):
        self.domain = domain


    def top_google_search(self):
        for correct in search(self.domain, stop=10):
            url = urlparse(correct).netloc
            print(url, self.domain)
            if self.domain in url:
                return True
        return False