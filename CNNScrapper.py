from Scrapper import Scrapper
from bs4 import BeautifulSoup

class CNNScrapper(Scrapper):
    def __init__(self, url, keywords):
        url_args = {'size': '10', 'q': keywords}
        super().__init__(url, keywords, url_args, callback=self.parse_search_result)

    def parse_search_result(self, url, page_content):
        print("nobs received {}".format(len(page_content)))
        print(page_content)
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('div', {'class': 'cnn-search__result-thumbnail'})
        print("found {} results on cnn".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = Scrapper(lnk, callback=self.parse_page_content)
            sc.start()

    def parse_page_content(self,url, page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': ['ObsArticle-body','flex-item-fluid']})
        # print("parsing page {}".format(url))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                # print(parag.get_text())
                out_text.append(parag.get_text())
        print("read {} chars on {}".format(len(''.join(out_text)), url))
        super().add_record(url, ''.join(out_text))



