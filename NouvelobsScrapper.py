from StaticScrapper import StaticScrapper
from bs4 import BeautifulSoup


class NouvelobsStaticScrapper(StaticScrapper):
    def __init__(self, url, keywords):
        url_args = {'referer': 'nouvelobs', 'q': keywords}
        super().__init__(url, keywords, url_args, callback=self.parse_search_result)

    def parse_search_result(self, url, page_content, keywords):
        # print("nobs received {}".format(len(page_content)))
        soup = BeautifulSoup(page_content, "lxml")
        # look for result links
        resdivs = soup.find_all('article', {'class': 'obs-resultat-article'})
        print("found {} results on nobs".format(len(resdivs)))
        for i in resdivs:
            lnk = i.find_all('a')[0].get('href')
            sc = StaticScrapper(lnk, keywords=keywords,callback=self.parse_page_content)
            sc.start()

    def parse_page_content(self,url, page_content,keywords):
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

        print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text))



