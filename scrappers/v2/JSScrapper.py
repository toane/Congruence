
from utils.printdebug import mute_print
print = mute_print(print)


from threading import Thread
from utils.DBFace import DBFace
from threading import Thread


from .StaticScrapper import StaticScrapper

try:
    from urllib import urlencode
except ImportError as ie:
    from urllib.parse import urlencode


class JSScrapper(Thread):
    def __init__(self, url, keywords=None, url_args=None, callback=None, js=True, requested_by=None):
        Thread.__init__(self)
        self.requested_by = requested_by
        assert callable(callback) is True or callback is None
        self.url = url
        self.request_url = ''
        self.callback = callback
        self.url_args = url_args
        self.keywords = keywords
        self.js = js  # if true, use the selenium framework to get content generated from js
        self.dbf = DBFace()
        if requested_by is not None and callable(requested_by):
            requested_by(self)

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
