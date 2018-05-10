from socket import gaierror
from threading import Thread
from DBFace import DBFace
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests

class StaticScrapper(Thread):
    def __init__(self, url, keywords=None, url_args=None, callback=None):
        Thread.__init__(self)
        # assert callable(callback) is True or callback is None
        self.url = url
        self.request_url = ''
        self.callback = callback
        self.url_args = url_args
        self.keywords = keywords
        self.dbf = DBFace()

    def parse_search_result(self, url, page_content, keywords):
        raise NotImplementedError

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            self.request_url = self.url + encoded_args
        except TypeError as te:
            self.request_url = self.url
            pass
        # print('StaticScrapper.run requesting {} with callback {}'.format(self.request_url, self.callback))
        # print('url hash: {}'.format(self.get_hash(request_url)))
        try:
            r = requests.get(self.request_url)
            if self.callback is not None:
                self.callback(self.url, r.text, self.keywords)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce.message)
