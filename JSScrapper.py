from socket import gaierror
from threading import Thread
from StaticScrapper import StaticScrapper
from DBFace import DBFace
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions

class JSScrapper(Thread):
    def __init__(self, url, keywords=None, url_args=None, callback=None, js=True):
        Thread.__init__(self)
        assert callable(callback) is True or callback is None
        self.url = url
        self.request_url = ''
        self.callback = callback
        self.url_args = url_args
        self.keywords = keywords
        self.js = js  # if true, use the selenium framework to get content generated from js
        self.dbf = DBFace()

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            self.request_url = self.url + encoded_args
        except TypeError as te:
            self.request_url = self.url
            pass
        # print('JSScrapper.run requesting {} with callback {}'.format(self.request_url, self.callback))
        if self.js is True:
            self.callback(self.request_url,keywords=self.keywords)
        else:
            sc = StaticScrapper(self.request_url, keywords=self.keywords,callback=self.callback)
            sc.start()