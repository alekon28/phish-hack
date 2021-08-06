from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import urlparse


class Base64Analyzer(object):
    def __init__(self, url: str):
        self.url = url

    def base64_image_detect(self):
        try:
            html_doc = urllib.request.urlopen(self.url).read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            linklist = soup.find_all("img")
            for link in linklist:
                src = link.get("src")
                if 'base64' in src:
                    return True
        except:
            return False
        else:
            return False
