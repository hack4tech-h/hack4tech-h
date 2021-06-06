from common.query import Query


class RapidDNS(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Dataset'
        self.source = 'RapidDNSQuery'

    def query(self):
        """
        Query the subdomain from the interface and do subdomain matching
                 """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        url = f'http://rapiddns.io/subdomain/{self.domain}'
        params = {'full': '1'}
        resp = self.get(url, params)
        self.subdomains = self.collect_subdomains(resp)

    def run(self):
        """
        Class execution entry
        """
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
        query = RapidDNS(domain)
        query.run()

    if __name__ == '__main__':
        run('example.com')