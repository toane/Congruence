from socket import gaierror
from threading import Thread
from pymongo import MongoClient
try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode
from urllib3 import HTTPSConnectionPool, make_headers, exceptions
import requests
import hashlib
import codecs
import os


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
        print('requesting {} with callback {}'.format(request_url, self.callback))
        # print('url hash: {}'.format(self.get_hash(request_url)))
        try:
            r = requests.get(request_url)
            if self.callback is not None:
                self.callback(self.url, r.text)
            return r.text
        except requests.exceptions.ConnectionError as ce:
            print(ce.message)

    def get_hash(self, url):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def write_file(self, url, content):
        if len(content) > 0:  # dont write empty strings
            with codecs.open(os.path.join("scrapped_data", self.get_hash(url)+'.txt').encode('utf-8'),'w', encoding='utf-8') as f:
                f.write(content)

    def add_record(self, url, content):
        pass
        # client = MongoClient('localhost', 27017)
        # db = client.mdb
        # coll = db.articol
        # coll.insert_one({self.get_hash(url): content})


