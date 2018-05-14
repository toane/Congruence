from bs4 import BeautifulSoup

from scrappers.StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote


class BBCScrapper(StaticScrapper):
    def __init__(self, url, keywords,requested_by, debug=False):
        self.requested_by = requested_by
        url_args = {'q': keywords}
        self.debug = debug
        self.lang = "en"
        super().__init__(url, keywords, url_args, callback=self.parse_search_result, requested_by=requested_by)

    def parse_search_result(self, url, page_content, keywords):
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('article')
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            sc = StaticScrapper(lnk, keywords=keywords, callback=self.parse_page_content,requested_by=self.requested_by)
            sc.start()

    def parse_page_content(self, url, page_content, keywords):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'story-body__inner'})
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(" " + pt)

        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text), lang=self.lang)
