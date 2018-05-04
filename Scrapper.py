from socket import gaierror
from threading import Thread
from pymongo import MongoClient
from StorageModel import StorageModel
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
    def __init__(self, url, keywords=None, url_args=None, callback=None):
        Thread.__init__(self)
        # assert callable(callback) is True or callback is None
        self.url = url
        self.request_url = ''
        self.callback = callback
        self.url_args = url_args
        self.keywords = keywords

    def run(self):
        try:
            encoded_args = urlencode(self.url_args)
            self.request_url = self.url + encoded_args
        except TypeError as te:
            self.request_url = self.url
            pass
        print('requesting {} with callback {}'.format(self.request_url, self.callback))
        # print('url hash: {}'.format(self.get_hash(request_url)))
        try:
            r = requests.get(self.request_url)
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
        new_record = StorageModel(self.keywords, url, content)
        print(new_record.mongo_value)
        client = MongoClient('localhost', 27017)
        db = client.mdb
        coll = db.articol
        coll.insert_one(new_record.mongo_value)


