from Scrapper import Scrapper
from bs4 import BeautifulSoup

class VingtMinutesScrapper(Scrapper):
    def __init__(self, url, keywords):
        url_args = {'q': keywords}
        super(VingtMinutesScrapper,self).__init__(url, url_args, self.parse_search_result)

    def parse_search_result(self, url, page_content):
        print("20min received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('div', {'class': ['gs-webResult','gsc-result']}) #TODO NO GOOD
        print("found {} results on 20min".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = Scrapper(lnk, self.parse_page_content)
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



