from bs4 import BeautifulSoup

from .StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class FigaroStaticScrapper(StaticScrapper):
    search_url = "http://recherche.lefigaro.fr/recherche/"
    
    def __init__(self, keywords, url = None, requested_by=None, debug=True):
        self.requested_by = requested_by
        self.debug = debug
        self.lang = "fr"
        super().__init__(keywords, url = url, requested_by=requested_by)

        
    @classmethod
    def make_search_params(cls, keywords):
        url = cls.search_url + quote(keywords)
        return (url, None)


    @staticmethod
    def parse_search_page(page_content):
        links = []
        # print("figaro received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        resdivs = soup.find_all('section', {'class': ['fig-profil',\
                                                      'fig-profil-mtpd',\
                                                      'fig-profil-std',\
                                                      'univers-figaro-vox']})
        print("found {} results on figaro".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            links.append(lnk)
        return links
    
    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'fig-content__body'})
        if len(content_p) == 0:
            # si pages sport
            content_p = soup.find_all('div', {'class': 's24-art-body'})
        if len(content_p) == 0:
            # si pages 'le particulier'
            content_p = soup.find_all('div', {'class': ['wysiwyg','classic']})
        if len(content_p) == 0:
            # si pages 'vin'
            content_p = soup.find_all('div', {'id': 'content-text'})
        if len(content_p) == 0:
            # pages 'figaro madame"
            content_p = soup.find_all('div', {'class': ['article-body',\
                                                        'mad__article__content__body',\
                                                        'selectionShareable']})
        if len(content_p) == 0:
            # pages 'economie'
            content_p = soup.find_all('div', {'class': 'texte'})  # marche pas car len > 0

        if len(content_p) == 0:
            # pages l'etudiant
            content_p = soup.find_all('div', {'class': 'article__content'})

        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                out_text.append(parag.get_text())
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        return out_text
    
