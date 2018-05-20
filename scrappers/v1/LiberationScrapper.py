from bs4 import BeautifulSoup
try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote, urlparse, parse_qs

from scrappers.v1.StaticScrapper import StaticScrapper


class LiberationStaticScrapper(StaticScrapper):
    def __init__(self, url, keywords, requested_by):
        self.requested_by = requested_by
        url_args = {'q': keywords}
        self.lang = "fr"
        super().__init__(url, keywords, url_args, callback=self.parse_search_result, requested_by=requested_by)

    def parse_search_result(self, url, page_content, keywords):
        # print("libe received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('div', {'class': 'live-content-right'})
        print("found {} results on libe".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            netloc = urlparse(lnk).netloc
            lnktxt = i.get_text()
            # print(lnk, netloc)
            if len(netloc) > 0:
                url_pref = ''
            else:
                url_pref = "http://www.liberation.fr"
            sc = StaticScrapper(url_pref + lnk, keywords=keywords, callback=self.parse_page_content,requested_by=self.requested_by)
            sc.start()

    def parse_page_content(self, url, page_content, keywords):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        # print("parsing page {}".format(url))
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': ['article-body','read-left-padding']})
        # print("libe page {} div on {}".format(len(content_p), url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(pt)
        # print("read {} chars on {}".format(len(''.join(out_text)),url))
        self.dbf.add_record(keywords, url, ''.join(out_text),lang=self.lang)