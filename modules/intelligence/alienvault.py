from common.query import Query


class AlienVault(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module ='Intelligence'
        self.source ='AlienVaultQuery'

    def query(self):
        """
        Query the subdomain from the interface and do subdomain matching
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)

        base ='https://otx.alienvault.com/api/v1/indicators/domain'
        dns = f'{base}/{self.domain}/passive_dns'
        resp = self.get(dns)
        self.subdomains = self.collect_subdomains(resp)

        url = f'{base}/{self.domain}/url_list'
        resp = self.get(url)
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
    query = AlienVault(domain)
    query.run()


if __name__ =='__main__':
    run('example.com')