from dns import resolver


class DNSAnalyzer(object):
    def __init__(self, domain: str):
        self.domain = domain

    def check_any_varification(self):
        verification_tags = ("facebook-domain-verification", "google-site-verification", 
                            "apple-domain-verification", "google-site-verification",
                            "yandex-verification","have-i-been-pwned-verification",
                            "mailru-verification","_globalsign-domain-verification")

        try:
            answers = resolver.resolve(self.domain, 'TXT')
            tags = []
        
            for answer in answers:
                for tag in verification_tags:
                    if tag in str(answer):
                        tags.append(str(answer))
        except:
            return []
        else:
            return tags


    def check_spf(self):
        spf_tags = ("v=spf1",)
        try:
            answers = resolver.resolve(self.domain, 'TXT')
            tags = []
        
            for answer in answers:
                for tag in spf_tags:
                    if tag in str(answer):
                        tags.append(str(answer))
        except:
            return []
        else:
            return tags

