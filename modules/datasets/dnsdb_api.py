from config import settings
from common.query import Query


class DNSdbAPI(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Dataset'
        self.source = 'DNSdbAPIQuery'
        self.addr = 'https://api.dnsdb.info/lookup/rrset/name/'
        self.api = settings.dnsdb_api_key

    def query(self):
        """
        Query the subdomain from the interface and do subdomain matching
                 """
        self.header = self.get_header()
        self.header.update({'X-API-Key': self.api})
        self.proxy = self.get_proxy(self.source)
        url = f'{self.addr}*.{self.domain}'
        resp = self.get(url)
        self.subdomains = self.collect_subdomains(resp)

    def run(self):
        """
        Class execution entry
        """
        if not self.have_api(self.api):
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
        query = DNSdbAPI(domain)
        query.run()

    if __name__ == '__main__':
        run('example.com')