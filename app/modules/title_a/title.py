import requests
from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import urlparse

class TitleAnalyzer(object):
    def __init__(self, url: str, domain: str):
        self.url = url
        self.domain = domain
        print(url)

    def check_title_in_google(self):
        try:
            page = requests.get(self.url, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')
            title = soup.find('title').string
        except Exception as e:
            return False
        else:
            for res in search(title, stop=10):
                url = urlparse(res).netloc
                if self.domain in url:
                    return True
                else:
                    return False
