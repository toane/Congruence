from bs4 import BeautifulSoup
try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote, urlparse, parse_qs

from .StaticScrapper import StaticScrapper


class LiberationStaticScrapper(StaticScrapper):
    search_url = "http://www.liberation.fr/recherche/?"
    
    def __init__(self, keywords, url = None, requested_by=None, debug=False):
        self.requested_by = requested_by
        self.debug = debug
        self.lang = "fr"
        super().__init__(keywords, url = url, requested_by=requested_by)

    @classmethod
    def make_search_params(cls, keywords):
        args = {'q': keywords}
        return (cls.search_url, args)
        
    @staticmethod
    def parse_search_page(page_content):
        links = []
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

            links.append(url_pref + lnk)
        return links

    @staticmethod
    def parse_page_content(page_content):
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
        return out_text
