from config import settings
from common.query import Query


class RiskIQ(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module ='Intelligence'
        self.source ='RiskIQAPIQuery'
        self.addr ='https://api.passivetotal.org/v2/enrichment/subdomains'
        self.user = settings.riskiq_api_username
        self.key = settings.riskiq_api_key

    def query(self):
        """
        Query the subdomain from the interface and do subdomain matching
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        params = {'query': self.domain}
        resp = self.get(url=self.addr,
                        params=params,
                        auth=(self.user, self.key))
        if not resp:
            return
        data = resp.json()
        names = data.get('subdomains')
        subdomain_str = str(set(map(lambda name: f'{name}.{self.domain}', names)))
        self.subdomains = self.collect_subdomains(subdomain_str)

    def run(self):
        """
        Class execution entry
        """
        if not self.have_api(self.user, self.key):
            return
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def run(domain):
    """
    Class uniform call entry

    :param str domain: domain name
    """
    query = RiskIQ(domain)
    query.run()


if __name__ =='__main__':
    run('alibabagroup.com')