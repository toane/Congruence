from socket import gaierror
from threading import Thread
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests


class Scrapper(Thread):
    def __init__(self, url, url_args, callback=None):
        Thread.__init__(self)
        # assert callable(callback) is True or callback is None
        self.url = url
        self.callback = callback
        self.url_args = url_args

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            request_url = self.url + encoded_args
        except TypeError as te:
            request_url = self.url
            pass
        # request_url = self.url + encoded_args
        print('requesting {} with callback {}'.format(request_url, self.callback))
        try:
            r = requests.get(request_url)
            if self.callback is not None:
                # print("calling {}".format(self.callback))
                if self.callback.func_code.co_argcount == 2:
                    self.callback(r.text)
                elif self.callback.func_code.co_argcount == 3:
                    self.callback(self.url, r.text)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce.message)

"""
class PageReader(Thread):
    def __init__(self, url, callback=None):
        
        :param url: url qui recevra la recherche
        :param url_params: url qui recevra la recherche
        :param keywords:
        :param callback:
        
        Thread.__init__(self)
        assert callable(callback) is True or callback is None
        self.url = url
        self.callback = callback

    def run(self):
        try:
            request_url = self.url
            print('requesting {}'.format(request_url))
            r = requests.get(request_url)
            self.callback(self.url, r.text)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            pass
"""