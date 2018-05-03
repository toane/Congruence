from Scrapper import Scrapper, PageReader
from bs4 import BeautifulSoup

class FigaroScrapper(Scrapper):
    def __init__(self, url, keywords):
        url = url+keywords
        super(FigaroScrapper,self).__init__(url, keywords, self.parse)

    def parse(self, e):
        print("figaro received {}".format(len(e)))
        soup = BeautifulSoup(e, "lxml")
        # look for result links
        # articles-list > section:nth-child(5)
        resdivs = soup.find_all('section', {'class': ['fig-profil','fig-profil-mtpd','fig-profil-std','univers-figaro-vox']})
        print("found {} results on figaro".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = PageReader(lnk, self.parse_page)
            sc.start()

    def parse_page(self,url, page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'fig-content__body'})
        print("parsing page {}".format(url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                out_text.append(parag.get_text())
        print("read {} chars on {}".format(len(''.join(out_text)), url))
