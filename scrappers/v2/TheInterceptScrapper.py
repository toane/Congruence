import re

from bs4 import BeautifulSoup
import json
from .StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote


class TheInterceptScrapper(StaticScrapper):
    search_url = "https://theintercept.com/api/requestSearchResults/?"
    search_args = {
            "page": 1,
            "postsPerPage": 20
    }
    
    def __init__(self, keywords, url = None, requested_by=None, debug=True):
        self.requested_by = requested_by
        self.debug = debug
        self.lang = "en"
        super().__init__(keywords, url = url, requested_by=requested_by)

    @classmethod
    def make_search_params(cls, keywords):
        args = dict(cls.search_args)
        args['searchTerm'] = keywords
        return (cls.search_url, args)

    @staticmethod
    def parse_search_page(page_content):
        dat = json.dumps(page_content)
        print("The intercept: {} results".format(len(page_content[0]))) # on ne regarde que dans le premier tableau de résultats
        links = [o['link'] for o in page_content[0]]
        return links
        
    
    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        # print("looking for content on {}".format(url))
        soup = BeautifulSoup(page_content, "lxml")
        tagtype = "div"
        tag_attr = "class"
        tag_attr_values = ['PostContent']
        # content_p = soup.find_all('div', {'class': 'story-body-supplemental'})
        content_p = soup.find_all(tagtype, {tag_attr: tag_attr_values})
        # print("found {} {} with {} {} on {}".format(len(content_p), tagtype, tag_attr,' '.join(tag_attr_values),url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(" " + pt)
        return out_text


if __name__ == '__main__':
    d = TheInterceptScrapper('https://theintercept.com/api/requestSearchResults/?', keywords="germany")
    d.start()