from socket import gaierror
from threading import Thread
from urllib.parse import urlencode,quote
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests


class Scrapper(Thread):
    def __init__(self, url, url_args, callback=None):
        """
        :param url: url qui recevra la recherche
        :param url_params: url qui recevra la recherche
        :param keywords:
        :param callback:
        """
        Thread.__init__(self)
        assert callable(callback) is True or callback is None
        self.url = url
        self.callback = callback
        self.url_args = url_args

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            request_url = self.url + encoded_args
            print('requesting {}'.format(request_url))
            r = requests.get(request_url)
            self.callback(r.text)
            return r.text
        except Exception as e:
            pass


class PageReader(Thread):
    def __init__(self, url, callback=None):
        """
        :param url: url qui recevra la recherche
        :param url_params: url qui recevra la recherche
        :param keywords:
        :param callback:
        """
        Thread.__init__(self)
        assert callable(callback) is True or callback is None
        self.url = url
        self.callback = callback

    def run(self):
        request_url = self.url
        print('requesting {}'.format(request_url))
        r = requests.get(request_url)
        self.callback(self.url, r.text)
        return r.text
