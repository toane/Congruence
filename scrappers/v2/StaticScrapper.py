from socket import gaierror
from threading import Thread

import urllib3

from utils.DBFace import DBFace
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests


class StaticScrapper(Thread):
    def __init__(self, keywords, url = None, requested_by=None, run = True):

        self.keywords = keywords
        self.url = url
        self.requested_by = requested_by
        
        if run:
            Thread.__init__(self)
            
        self.dbf = DBFace()
        if requested_by is not None and callable(requested_by):
            requested_by(self)

    
    def search(self):
        #url_args = self.search_args
        search_params = self.make_search_params(self.keywords)
        page_content = self.fetch_url(search_params[0], search_params[1])
        links = self.parse_search_page(page_content)
        print("found links : {}".format(links))

        for lnk in links:
            sc = self.__class__(keywords=self.keywords, url=lnk, requested_by=self.requested_by)
            sc.start()

    def content_to_db(self):
        page_content = self.fetch_url(self.url)
        text = self.parse_page_content(page_content)
        
        # print("read {} chars on {}".format(len(''.join(out_text)), url))
        self.dbf.add_record(self.keywords, self.url, ''.join(text), lang=self.lang)

    @classmethod
    def get_search_page(cls, keywords):
        print("k" ,keywords)
        search_params = cls.make_search_params(keywords)
        return cls.fetch(search_params[0], search_params[1])
    
    @staticmethod
    def fetch_url(url, url_args = None):
        try:
            encoded_args = urlencode(url_args)
            request_url = url + encoded_args
        except TypeError as te:
            request_url = url
            pass
        try:
            print("requesting url : ", request_url)
            r = requests.get(request_url)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except urllib3.exceptions.MaxRetryError as mre:
            print(mre)

    def run(self):
        if self.url is None:
            self.search()
        else:
            self.content_to_db()
            

