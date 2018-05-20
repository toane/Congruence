import os
import sys

print("path: ", sys.path)

from streamparse import Bolt

# from libs.scrappers.BBCScrapper import get_search_result as BBC_search_result
# from libs.scrappers.DiplomatScrapper import get_search_result as Diplo_search_result
# from libs.scrappers.NYTScrapper import  get_search_result as NYT_search_result

from scrappers.v2.BBCScrapper import BBCScrapper
from scrappers.v2.NYTScrapper import NYTScrapper
from scrappers.v2.DiplomatScrapper import DiplomatScrapper

from scrappers.v2.StaticScrapper import StaticScrapper

fetch = StaticScrapper.fetch_url
search_functions = {
    "BBC" :  BBCScrapper.get_search_page,
    "NYT" : NYTScrapper.get_search_page,
    "Diplo" : DiplomatScrapper.get_search_page
}

class OmniSearchBolt(Bolt):
    outputs = ['info', 'url']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.searched = set()
        self.name = conf["OmniSearchBoltName"]
        self.search_function = search_functions[self.name]

    def process(self, tup):
        info = tup.values[0]
        keyword = tup.values[1]

        
        res = self.search_function(keyword)
        self.logger.info("{} Search Bolt found : {}" \
                         .format(self.name, res))
        for url in res:
            if url not in self.searched:
                self.searched.add(url)
                self.emit([info, url])
