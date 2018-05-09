import re

from StaticScrapper import StaticScrapper
from bs4 import BeautifulSoup
try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class NYTScrapper(StaticScrapper):
    def __init__(self, url, keywords, debug=True):
        url = url+quote(keywords)
        self.debug = debug
        super().__init__(url, keywords, callback=self.parse_search_result)

    def parse_search_result(self, url, page_content, keywords):
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('li', {'class': re.compile("(SearchResults-item*)")})
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            sc = StaticScrapper("http://www.nytimes.com" + lnk, keywords=keywords, callback=self.parse_page_content)
            sc.start()

    def parse_page_content(self, url, page_content, keywords):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'story-body-supplemental'})
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(pt)

        content_p = soup.find_all('p', {'class': ['css-n7ezar','e2kc3sl0']})
        # print("extra {}".format(len(content_p)))
        for maincnt in content_p:
            pt = maincnt.get_text()
            out_text.append(pt)
        print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text))