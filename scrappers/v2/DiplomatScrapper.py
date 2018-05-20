import json

from bs4 import BeautifulSoup

from .StaticScrapper import StaticScrapper

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import urlencode, quote, urlparse, parse_qs

class DiplomatScrapper(StaticScrapper):
    search_url = 'https://www.googleapis.com/customsearch/v1element?'
    search_args = {
        'key': "AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY",
        'rsz': "filtered_cse",
        'num': 10,
        'hl': "en",
        'prettyPrint': "false",
        'source': "gcsc",
        'gss': ".com",
        'sig': "d5630e36052d1355ead71530c29be9ea",
        'cx': "006972344228181832854:w07k6emi2wk",
        'cse_tok': "ABPF6HjAnG5F-oJ6m6bhPdqFeqLbLiqrMw:1526570098210",
    }
    
    def __init__(self, keywords, url = None, requested_by=None):
        self.requested_by = requested_by
        super().__init__(keywords, url = url, requested_by=requested_by)
        self.lang = "en"
        
    @classmethod
    def make_search_params(cls, keywords):
        args = dict(cls.search_args)
        args['q'] = keywords
        return (cls.search_url, args)
    
    @staticmethod
    def parse_search_page(page_content):
        links = []
        #print("The Diplomat: got {} chars".format(len(page_content)))
        result = json.loads(page_content)
        if 'error' in result.keys():
            print("TheDiplomatScrapper: "+ result['error']['errors'][0]['message'])
            print("obsolete cse_tok parameter ?")
        else:
            for i in result['results']:
                lnk = i['clicktrackUrl']
                query_part = urlparse(lnk).query
                query_comps = parse_qs(query_part)
                lnk = query_comps['q'][0]
                links.append(lnk)
        return links

    @staticmethod
    def parse_page_content(page_content):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'itemprop': ['articleBody']})
        # print("Diplomat: found {} article elem".format(len(content_p)))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                pt = parag.get_text()
                out_text.append(pt)
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        return out_text
    

if __name__ == '__main__':
    d = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keywords="france")
    d.start()
