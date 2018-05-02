from Scrapper import Scrapper, PageReader
from bs4 import BeautifulSoup

class LiberationScrapper(Scrapper):
    def __init__(self, url, keywords):
        super().__init__(url, keywords, self.parse)

    def parse(self, e):
        print("libe received {}".format(len(e)))
        soup = BeautifulSoup(e, "lxml")
        # look for result links
        resdivs = soup.find_all('div', {'class': 'live-content-right'})
        print("found {} results on libe".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            lnktxt = i.get_text()
            sc = PageReader("http://www.liberation.fr"+lnk, self.parse_page)
            sc.start()

    def parse_page(self, url, page_content):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        print("parsing page {}".format(url))
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'wysiwyg'})
        print("libe page {} div on {}".format(len(content_p), url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                pt = parag.get_text()
                out_text.append(pt)
        print("read {} chars on {}".format(len(''.join(out_text)),url))

