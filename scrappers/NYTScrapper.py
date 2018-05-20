import re

from bs4 import BeautifulSoup

from scrappers.StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class NYTScrapper(StaticScrapper):
    search_url = "https://www.nytimes.com/search/"
    
    def __init__(self, url, keywords, requested_by, debug=True):
        self.requested_by = requested_by
        url = url+quote(keywords)
        self.debug = debug
        self.lang = "en"
        super().__init__(url, keywords, callback=self.search_and_scrap, requested_by=requested_by)

    @classmethod
    def get_search_page(keywords):
        return self.fetch(self.search_url + quote(keywords))
        
    @staticmethod
    def parse_search_page(page_content):
        links = []
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('li', {'class': re.compile("(SearchResults-item*)")})
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            if not "nytimes.com" in lnk:
                lnk = "http://www.nytimes.com" + lnk
            links.append(lnk)
        return links
        
    
    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        # print("looking for content on {}".format(url))
        soup = BeautifulSoup(page_content, "lxml")
        tagtype = "div"
        tag_attr = "class"
        tag_attr_values = ['story-body-supplemental']
        # content_p = soup.find_all('div', {'class': 'story-body-supplemental'})
        content_p = soup.find_all(tagtype, {tag_attr: tag_attr_values})
        # print("found {} {} with {} {} on {}".format(len(content_p), tagtype, tag_attr,' '.join(tag_attr_values),url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(" " + pt)

        tagtype = "p"
        tag_attr = "class"
        tag_attr_values = ['css-n7ezar','e2kc3sl0']
        # content_p = soup.find_all('p', {'class': ['css-n7ezar','e2kc3sl0']})
        content_p = soup.find_all(tagtype, {tag_attr: tag_attr_values})
        # print("found {} {} with {} {} on {}".format(len(content_p), tagtype, tag_attr, ' '.join(tag_attr_values), url))
        for maincnt in content_p:
            pt = maincnt.get_text()
            out_text.append(" " + pt)
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        return out_text

    
    def search_and_scrap(self, url, page_content, keywords):
        links = NYTScrapper.parse_search_page(page_content)
        for lnk in links:
            sc = StaticScrapper(lnk, keywords=keywords, callback=self.get_page_content, requested_by=self.requested_by)
            sc.start()

    def get_page_content(self, url, page_content, keywords):
        text = ''.join(NYTScrapper.parse_page_content(page_content))
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, text, lang=self.lang)
        
