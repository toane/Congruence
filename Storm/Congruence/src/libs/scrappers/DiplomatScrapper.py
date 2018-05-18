import json

from bs4 import BeautifulSoup

from libs.scrappers.StaticScrapper import fetch_url

from urllib.parse import urlparse, parse_qs


def get_search_result(keywords):

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
        'q' : keywords
    }


    urls = []

    page_content = fetch_url(search_url, search_args)
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
            urls.append(lnk)

    return urls

def get_page_content(page_url):
    page_content = fetch_url(page_url)
    out_text = []
    soup = BeautifulSoup(page_content, "lxml")
    content_p = soup.find_all('div', {'itemprop': ['articleBody']})
    # print("Diplomat: found {} article elem".format(len(content_p)))
    for maincnt in content_p:
        for parag in maincnt.find_all('p'):
            pt = parag.get_text()
            out_text.append(pt)
    return out_text
