import re

from bs4 import BeautifulSoup

from libs.scrappers.StaticScrapper import fetch_url

try:
    from urllib import quote
except ImportError as ie:
    from urllib.parse import quote

        
def get_search_result(keywords):
    search_url = "https://www.nytimes.com/search/"
    page_content = fetch_url(search_url + quote(keywords), "")
    links = []
    soup = BeautifulSoup(page_content, "lxml")
    # look for result links
    resdivs = soup.find_all('li', {'class': re.compile("(SearchResults-item*)")})
    for i in resdivs:
        # TODO manage full urls like http://query.nytimes.com/gst/abstract.html?res=990CEEDC1539E433A25757C0A9679C946196D6CF
        lnk = i.find_all('a')[0].get('href')
        lnktxt = i.get_text()
        if not "nytimes.com" in lnk:
            links.append("http://www.nytimes.com" + lnk)

    return links


# TODO : ajouter un espace entre les paragraphes </p><p>
def get_page_content(page_url):
    page_content = fetch_url(page_url)
    out_text = []
    # print("looking for content on {}".format(url))
    soup = BeautifulSoup(page_content, "lxml")
    tagtype = "div"
    tag_attr = "class"
    tag_attr_values = ['story-body-supplemental']
    # content_p = soup.find_all('div', {'class': 'story-body-supplemental'})
    content_p = soup.find_all(tagtype, {tag_attr: tag_attr_values})
    # print("found {} {} with {} {} on {}".format(len(content_p), tagtype, tag_attr,' '.join(tag_attr_values),url))
    for maincnt in content_p:
        for parag in maincnt.find_all('p'):
            pt = parag.get_text()
            out_text.append(" " + pt)

    tagtype = "p"
    tag_attr = "class"
    tag_attr_values = ['css-n7ezar','e2kc3sl0']
    # content_p = soup.find_all('p', {'class': ['css-n7ezar','e2kc3sl0']})
    content_p = soup.find_all(tagtype, {tag_attr: tag_attr_values})
    # print("found {} {} with {} {} on {}".format(len(content_p), tagtype, tag_attr, ' '.join(tag_attr_values), url))
    for maincnt in content_p:
        pt = maincnt.get_text()
        out_text.append(" " + pt)

    return out_text
