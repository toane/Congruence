from bs4 import BeautifulSoup

from scrappers.v1.StaticScrapper import StaticScrapper
from utils.DBFace import DBFace

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class FigaroStaticScrapper(StaticScrapper):
    def __init__(self, url, keywords, requested_by):
        self.requested_by = requested_by
        url = url+quote(keywords)
        super().__init__(url, keywords,'', callback=self.parse_search_result, requested_by=requested_by)
        self.lang = "fr"
        self.dbf = DBFace()

    def parse_search_result(self, url, page_content, keywords):
        # print("figaro received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        resdivs = soup.find_all('section', {'class': ['fig-profil',\
                                                      'fig-profil-mtpd',\
                                                      'fig-profil-std',\
                                                      'univers-figaro-vox']})
        print("found {} results on figaro".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = StaticScrapper(lnk, keywords=keywords, callback=self.parse_page_content,requested_by=self.requested_by)
            sc.start()

    def parse_page_content(self,url, page_content, keywords):
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
        self.dbf.add_record(keywords, url, ''.join(out_text),lang=self.lang)
