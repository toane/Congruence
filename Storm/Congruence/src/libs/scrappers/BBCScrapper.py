from bs4 import BeautifulSoup

from libs.scrappers.StaticScrapper import fetch_url

    

def get_search_result(keywords):
    search_url = "https://www.bbc.co.uk/search?"
    search_args = {'q': keywords}
    urls = []

    page_content = fetch_url(search_url, search_args)
    soup = BeautifulSoup(page_content, "lxml")
    # look for result links
    resdivs = soup.find_all('article')
    for i in resdivs:
        lnk = i.find_all('a')[0].get('href')
        lnktxt = i.get_text()
        urls.append(lnk)

    return urls

def get_page_content(page_url):
    page_content = fetch_url(page_url)
    out_text = []
    soup = BeautifulSoup(page_content, "lxml")
    content_p = soup.find_all('div', {'class': 'story-body__inner'})


    for maincnt in content_p:
        for parag in maincnt.find_all('p'):
            pt = parag.get_text()
            out_text.append(" " + pt)

    return out_text
