import time
from config.log import logger
from common.query import Query


class WZPCQuery(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Dataset'
        self.source = 'WZPCQuery'

    def query(self):
        """
        Query the subdomain from the interface and do subdomain matching
                """

        base_addr = 'http://114.55.181.28/check_web/' \
                    'databaseInfo_mainSearch.action'
        page_num = 1
        while True:
            time.sleep(self.delay)
            self.header = self.get_header()
            self.proxy = self.get_proxy(self.source)
            params = {'isSearch': 'true', 'searchType': 'url',
                      'term': self.domain, 'pageNo': page_num}
            try:
                resp = self.get(base_addr, params)
            except Exception as e:
                logger.log('ERROR', e.args)
                break
            if not resp:
                break
            subdomains = self.match_subdomains(resp.text)
            if not subdomains:  # Stop querying if no subdomains are found
                break
            self.subdomains.update(subdomains)
            if not subdomains:
                break
            if page_num > 10:
                break
            page_num += 1

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
        query = WZPCQuery(domain)
        query.run()

    if __name__ == '__main__':
        run('sc.gov.cn')
        run('bkzy.org')