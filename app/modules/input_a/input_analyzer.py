import requests
from bs4 import BeautifulSoup

class InputAnalyzer(object):
    def __init__(self, url: str):
        self.url = url
        print(url)

    def check_for_any_input_on_page(self):
        try:
            page = requests.get(self.url, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')

            if len(soup.find_all('input') + soup.find_all('form')):
                return True
        except Exception as e:
            print(f"Error {e}")
            return False

