import re
import dns
import validators
import requests
from urllib.parse import urlparse

from validators.domain import domain
from app.modules.dns_a.dns_analyzer import DNSAnalyzer



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
        report = {}

        dns_a = DNSAnalyzer(self.domain)
        report["verifications_tags"] = dns_a.check_any_varification()
        report["spf_tags"] = dns_a.check_spf()
        report["verifications_tags_count"] = len(report["verifications_tags"])

        
    
        return {"status": "success", "report": report}


    def validate_link(self, link):
        if validators.domain(link):
            self.domain = link
            self.link = None
            return True
        elif validators.url(link):
            self.domain = urlparse(link).netloc
            return True
        else:
            return False
                
                

            
            print("is link")
            return True

    def check_connection(self):
        if self.link is None:
            r = requests.get(f"http://{self.domain}")
            if r.status_code != 200:
                return False
            else:
                return True

        elif self.domain is None:
            r = requests.get(self.link)
            if r.status_code != 200:
                
                return False
            else:
                return True

        else:
            return True

       

