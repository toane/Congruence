from bs4 import BeautifulSoup

from .StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote


    
class BBCScrapper(StaticScrapper):
    search_url = "https://www.bbc.co.uk/search?"
    search_args = {"filter" : "news"}
    
    def __init__(self, keywords, url = None, requested_by=None, debug=False):
        self.requested_by = requested_by
        self.debug = debug
        self.lang = "en"
        super().__init__(keywords, url = url, requested_by=requested_by)

    @classmethod
    def make_search_params(cls, keywords):
        args = dict(cls.search_args)
        args['q'] = keywords
        return (cls.search_url, args)
        
        
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
    
