import re

from bs4 import BeautifulSoup

from scrappers.StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class NYTScrapper(StaticScrapper):
    def __init__(self, url, keywords, requested_by, debug=True):
        self.requested_by = requested_by
        url = url+quote(keywords)
        self.debug = debug
        self.lang = "en"
        super().__init__(url, keywords, callback=self.parse_search_result, requested_by=requested_by)

    def parse_search_result(self, url, page_content, keywords):
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('li', {'class': re.compile("(SearchResults-item*)")})
        for i in resdivs:
            # TODO manage full urls like http://query.nytimes.com/gst/abstract.html?res=990CEEDC1539E433A25757C0A9679C946196D6CF
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            sc = StaticScrapper("http://www.nytimes.com" + lnk, keywords=keywords, callback=self.parse_page_content,requested_by=self.requested_by)
            sc.start()


    # TODO : ajouter un espace entre les paragraphes </p><p>
    def parse_page_content(self, url, page_content, keywords):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        print("looking for content on {}".format(url))
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
        self.dbf.add_record(keywords, url, ''.join(out_text), lang=self.lang)
