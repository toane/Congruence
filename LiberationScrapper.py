from Scrapper import Scrapper
from bs4 import BeautifulSoup

class LiberationScrapper(Scrapper):
    def __init__(self, url, keywords):
        url_args = {'q': keywords}
        super().__init__(url, keywords, url_args, callback=self.parse_search_result)

    def parse_search_result(self, url, page_content):
        print("libe received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('div', {'class': 'live-content-right'})
        print("found {} results on libe".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href') #TODO si url trouvee complete, ne pas ajouter www.liberation.fr
            lnktxt = i.get_text()
            sc = Scrapper("http://www.liberation.fr"+lnk, callback=self.parse_page_content)
            sc.start()

    def parse_page_content(self, url, page_content):
        out_text = []
        """
        :param e contient le texte d'une page de resultat
        :return:
        """
        # print("parsing page {}".format(url))
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': ['article-body','read-left-padding']})
        print("libe page {} div on {}".format(len(content_p), url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                pt = parag.get_text()
                out_text.append(pt)
        print("read {} chars on {}".format(len(''.join(out_text)),url))
        super().add_record(url, ''.join(out_text))