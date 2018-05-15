import json

from bs4 import BeautifulSoup

from DBFace import DBFace
from scrappers.StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote

class DiplomatScrapper(StaticScrapper):
    def __init__(self, url, keywords, requested_by=None):
        self.requested_by = requested_by
        url_args = {
            'key': "AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY",
            'rsz': "filtered_cse",
            'num': 10,
            'hl': "en",
            'prettyPrint': "false",
            'source': "gcsc",
            'gss': ".com",
            'sig': "d5630e36052d1355ead71530c29be9ea",
            'cx': "006972344228181832854:w07k6emi2wk",
            'cse_tok': "ABPF6HiJS9U2hAV6jNb1_iidY_voUdQW8w:1526388826953",
            "q": keywords
        }
        super().__init__(url, keywords, url_args, callback=self.parse_search_result, requested_by=requested_by)
        self.lang = "en"
        self.dbf = DBFace()

    def parse_search_result(self, url, page_content, keywords):
        print("Diplomat: got {} chars".format(len(page_content)))
        result = json.loads(page_content)
        print(page_content)
        for i in result['results']:
            lnk = i['clicktrackUrl']
            sc = StaticScrapper(lnk, keywords=keywords, callback=self.parse_page_content, requested_by=self.requested_by)
            sc.start()

    def parse_page_content(self,url, page_content, keywords):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'itemprop': ['articleBody']})
        # print("Diplomat: found {} article elem".format(len(content_p)))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(pt)
        print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text), lang=self.lang)


if __name__ == '__main__':
    d = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keywords="france")
    d.start()