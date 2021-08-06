from app.modules.title_a.title import TitleAnalyzer
import validators
import requests
from urllib.parse import urlparse
from validators.domain import domain

from app.modules.weight_config import weigths
from app.modules.dns_a.dns_analyzer import DNSAnalyzer
from app.modules.google_search_a.search_analyzer import SearchAnalyzer
from app.modules.input_a.input_analyzer import InputAnalyzer
from app.modules.tls_a.tls_analyzer import TLSAnalyzer
from app.modules.static_a.static_analyzer import StaticAnalyzer
from app.modules.base64_a.base64_analyzer import Base64Analyzer


class BaseAnalyzer(object):
    #Result statuses
    CLEAN: str = "clean"
    SUSPECT: str = "suspect"
    PHISHING: str = "phishing"

    def __init__(self, link):
        self.link = link
        self.report = {}
        self.domain = None
        
    def get_report(self):
        if not self.validate_link(self.link):
            return {"status": "error", "info": "Invalid link"}
        if not self.check_connection():
            return {"status": "error", "info": "Site unreachabel"}

        dns_a = DNSAnalyzer(self.domain)
        search_a = SearchAnalyzer(self.domain)
        input_a = InputAnalyzer(self.link)
        tls_a = TLSAnalyzer(self.link)
        static_a = StaticAnalyzer(self.domain)
        title_a = TitleAnalyzer(self.link, self.domain)
        base64_a = Base64Analyzer(self.link)

        self.report["verifications_tags"] = dns_a.check_any_varification()
        self.report["spf_tags"] = dns_a.check_spf()
        self.report["verifications_tags_count"] = len(self.report["verifications_tags"])
        self.report["top_google_search"] = search_a.top_google_search()
        self.report["page_contain_inputs"] = input_a.check_for_any_input_on_page()
        self.report["use_tls"] = tls_a.verify_tls()
        self.report["in_phish_base"] = static_a.check_in_static_base()
        self.report["title_in_google"] = title_a.check_title_in_google()
        self.report["base64_detect"] = base64_a.base64_image_detect()
    
        return {"status": "success", "report": self.report}

    def validate_link(self, link):
        if validators.domain(link):
            self.domain = link
            self.link = f"https://{link}"
            return True
        elif validators.url(link):
            self.domain = urlparse(link).netloc
            if self.link != "s":
                self.link = "https" + self.link[4:len(self.link)]
            return True
        else:
            return False
                
    def check_connection(self):
        try:
            r = requests.get(f"http://{self.domain}")
            if r.status_code != 200:
                return False
            else:
                return True
        except:
            return False
        else:
            raise Exception("conn_error")

       
    def get_verdict(self):
        points = 1
        status = self.CLEAN

        if self.report["verifications_tags_count"] > 1:
            return 1
        elif self.report["verifications_tags_count"] == 0:
            points *= weigths["verifications_tags_count"]

        if not self.report["spf_tags"]:
            points *= weigths["spf_tags"]

        if not self.report["top_google_search"]:
            points *= weigths["top_google_search"]

        if self.report["page_contain_inputs"] and not self.report["use_tls"]:
            points *= weigths["page_contain_inputs"] * weigths["use_tls"] * 0.5

        if self.report["in_phish_base"]:
            points *= weigths["in_phish_base"]

        if not self.report["title_in_google"]:
            points *= weigths["title_in_google"]

        if self.report["base64_detect"]:
            points *= weigths["base64_detect"]
       
        return points