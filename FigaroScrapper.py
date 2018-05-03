from Scrapper import Scrapper, PageReader
from bs4 import BeautifulSoup
from urllib import quote

class FigaroScrapper(Scrapper):
    def __init__(self, url, keywords):
        url = url+quote(keywords)
        super(FigaroScrapper,self).__init__(url, keywords, self.parse)

    def parse(self, e):
        print("figaro received {}".format(len(e)))
        soup = BeautifulSoup(e, "lxml")
        resdivs = soup.find_all('section', {'class': ['fig-profil',\
                                                      'fig-profil-mtpd',\
                                                      'fig-profil-std',\
                                                      'univers-figaro-vox']})
        print("found {} results on figaro".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = PageReader(lnk, self.parse_page)
            sc.start()

    def parse_page(self,url, page_content):
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

        # print("parsing page {}".format(url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                out_text.append(parag.get_text())
        print("read {} chars on {}".format(len(''.join(out_text)), url))
