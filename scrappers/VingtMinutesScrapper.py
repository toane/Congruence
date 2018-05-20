from scrappers.StaticScrapper import StaticScrapper
from bs4 import BeautifulSoup

from scrappers.JSScrapper import JSScrapper

try:
    from selenium import webdriver
except ImportError as ie:
    print("python: selenium module unavailable, 20min dynamic content scraping disabled")

try:
    from selenium.common.exceptions import WebDriverException
except ImportError:
    pass


class VingtMinutesScrapper(JSScrapper):

    def __init__(self, url, keywords):
        url_args = {'q': keywords}
        self.lang = "fr"
        super().__init__(url, keywords, url_args, callback=self.parse_search_result)

    def parse_search_result(self, full_url_query, keywords):
        try:
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
            driver.get(full_url_query)            # look for search results

            result_cells = driver.find_elements_by_css_selector('td.gsc-table-cell-snippet-close')
            print("found {} results on 20min".format(len(result_cells)))
            # pull url from each WebDriver element
            for c in result_cells:
                url = c.find_element_by_tag_name('a').get_attribute('href')
                # download static html page content
                jss = StaticScrapper(url, keywords=keywords, callback=self.parse_page_content)
                jss.start()
        except WebDriverException as wde:
            print(wde)

    def parse_page_content(self,url, page_content, keywords):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        # content_p = soup.find_all('div', {'class': ['lt-endor-body' 'content']})
        content_p = soup.find_all('div', {'class': ['lt-endor-body content']})
        print("20min {} content div found".format(len(content_p)))
        for maincnt in content_p:
            for parag in maincnt.find_all('p'):
                out_text.append(parag.get_text())
        print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text),lang=self.lang)
