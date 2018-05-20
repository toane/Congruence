from .StaticScrapper import StaticScrapper
from bs4 import BeautifulSoup


class NouvelobsStaticScrapper(StaticScrapper):
    search_url = "https://recherche.nouvelobs.com/?"
    
    def __init__(self, keywords, url = None, requested_by=None, debug=False):
        self.requested_by = requested_by
        self.debug = debug
        self.lang = "fr"
        super().__init__(keywords, url = url, requested_by=requested_by)


    @classmethod
    def make_search_params(cls, keywords):
        args = {'referer': 'nouvelobs', 'q': keywords}
        return (cls.search_url, args)

    @staticmethod
    def parse_search_page(page_content):
        links = []
        # print("nobs received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('article', {'class': 'obs-resultat-article'})
        print("found {} results on nobs".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            links.append(lnk)
        return links

    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': ['ObsArticle-body','flex-item-fluid']})
        # print("parsing page {}".format(url))
        for maincnt in content_p:
            out_text.append(maincnt.get_text())
            for parag in maincnt.find_all('p'):
                out_text.append(parag.get_text())

        content_p = soup.find_all('article', {'class': 'infos'})
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                out_text.append(parag.get_text())

        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        return out_text



