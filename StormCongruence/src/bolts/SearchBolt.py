import os
import sys

import config.config as config
config.init()

from streamparse import Bolt

from scrappers.v2.BBCScrapper import BBCScrapper
from scrappers.v2.NYTScrapper import NYTScrapper
from scrappers.v2.DiplomatScrapper import DiplomatScrapper


search_functions = {
    "BBC" :  BBCScrapper.get_search_results,
    "NYT" : NYTScrapper.get_search_results,
    "Diplo" : DiplomatScrapper.get_search_results
}

class SearchBolt(Bolt):
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
