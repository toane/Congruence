import os

from streamparse import Bolt
from bolts.scrappers.DiplomatScrapper import DiplomatScrapper 

class ScrapBolt(Bolt):
    outputs = ['keyword', 'url']

    def initialize(self, conf, ctx):

        self.pid = os.getpid()
        

    def process(self, tup):
        keyword = tup.values[0]
        scrapper = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keyword)
        res = scrapper.run()
        self.logger.info("found : {}".format(res))
        self.emit([(keyword, url) for url in res])
