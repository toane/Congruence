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
    def __init__(self, url, keywords=None, url_args=None, callback=None, requested_by=None):
        Thread.__init__(self)
        # assert callable(callback) is True or callback is None
        self.url = url
        self.request_url = ''
        self.callback = callback
        self.url_args = url_args
        self.keywords = keywords
        self.dbf = DBFace()
        self.requested_by = requested_by
        if requested_by is not None and callable(requested_by):
            requested_by(self)

    def parse_search_result(self, url, page_content, keywords):
        raise NotImplementedError

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            self.request_url = self.url + encoded_args
        except TypeError as te:
            self.request_url = self.url
            pass
        try:
            r = requests.get(self.request_url)
            if self.callback is not None:
                self.callback(self.url, r.text, self.keywords)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except urllib3.exceptions.MaxRetryError as mre:
            print(mre)
