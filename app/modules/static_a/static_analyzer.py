from urllib.parse import urlparse


class StaticAnalyzer(object):
    def __init__(self, domain: str):
        self.domain = domain
        self.static_base_path = "app/static_data/phish_url"

    def check_in_static_base(self):
        phish_flag = False
        file = open(self.static_base_path, "r")
        while True:
            line = file.readline()
            if not line:
                break
            if self.domain == urlparse(line.strip()).netloc:
                phish_flag = True
        file.close()
        if phish_flag:
            return True
        else:
            return False

    