from scrappers.StaticScrapper import StaticScrapper
from bs4 import BeautifulSoup

from scrappers.DynamicScrapper import JSScrapper

try:
    from selenium import webdriver
except ImportError as ie:
    print("python: selenium module unavailable, CNN dynamic content scraping disabled")

try:
    from selenium.common.exceptions import WebDriverException
except ImportError:
    pass


class CNNScrapper(JSScrapper):
    def __init__(self, url, keywords, requested_by):
        self.requested_by = requested_by
        self.url_args = {'size': '10', 'q': keywords}
        self.lang = "en"
        super().__init__(url, keywords, self.url_args, callback=self.parse_search_result, js=True, requested_by=requested_by)


    def parse_search_result(self, full_url_query, keywords):
        try:
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
            driver.get(full_url_query)
            # look for search results
            result_cells = driver.find_elements_by_css_selector('div.cnn-search__result-thumbnail')
            print("found {} results on cnn".format(len(result_cells)))
            # pull url from each WebDriver element
            for c in result_cells:
                url = c.find_element_by_tag_name('a').get_attribute('href')
                # download static html page content
                jss = StaticScrapper(url, keywords=keywords,callback=self.parse_page_content,requested_by=self.requested_by)
                jss.start()
        except NameError as ne:
            print("python: no webdriver available")

    def parse_page_content(self,url, page_content,keywords):
        out_text = []
        soup = BeautifulSoup(page_content, "lxml")
        content_p = soup.find_all('div', {'class': 'zn-body__paragraph'})
        for maincnt in content_p:
            out_text.append(maincnt.get_text())
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(keywords, url, ''.join(out_text), lang=self.lang)



