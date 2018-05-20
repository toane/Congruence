from bs4 import BeautifulSoup

from scrappers.StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote


class BBCScrapper(StaticScrapper):
    search_url = "https://www.bbc.co.uk/search?"
    search_args = {"filter" : "news"}
    
    def __init__(self, url, keywords, requested_by, debug=False):
        self.requested_by = requested_by
        url_args = dict(self.search_args)
        url_args['q'] = keywords
        self.debug = debug
        self.lang = "en"
        super().__init__(url, keywords, url_args, callback=self.search_and_scrap, requested_by=requested_by)

    @classmethod
    def get_search_page(keywords):
        args = dict(self.search_args)
        args['q'] = keywords
        return self.fetch(search_url, args)
        
    @staticmethod
    def parse_search_page(page_content):
        links = []
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('article')
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            links.append(lnk)
        return links
    
    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'story-body__inner'})
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(" " + pt)
        return out_text
    
    def search_and_scrap(self, url, page_content, keywords):
        links = BBCScrapper.parse_search_page(page_content)
        for lnk in links:
            sc = StaticScrapper(lnk, keywords=keywords, callback=self.get_page_content, requested_by=self.requested_by)
            sc.start()

    def get_page_content(self, url, page_content, keywords):
        text = ''.join(BBCScrapper.parse_page_content(page_content))
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, text, lang=self.lang)
        
