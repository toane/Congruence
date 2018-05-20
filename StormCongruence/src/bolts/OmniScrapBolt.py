import os
import sys

from streamparse import Bolt

from scrappers.v2.BBCScrapper import BBCScrapper
from scrappers.v2.NYTScrapper import NYTScrapper
from scrappers.v2.DiplomatScrapper import DiplomatScrapper


scrap_functions = {
    "BBC" :  BBCScrapper.get_scrap_results,
    "NYT" : NYTScrapper.get_scrap_results,
    "Diplo" : DiplomatScrapper.get_scrap_results
}


class OmniScrapBolt(Bolt):
    outputs = ['info', 'parag']
    

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.searched = set()
        self.name = conf["OmniScrapBoltName"]
        self.scrap_function = scrap_functions[self.name]
        self.scraped = set()

    def process(self, tup):
        info = tup.values[0]
        keyword = info["keyword"]
        url = tup.values[1]
        info['url'] = url

        if url in self.scraped:
            return
        self.scraped.add(url)
        res = self.scrap_function(url)

        if len(res) == 0:
            self.logger.info( \
                "{} Scrap Bolt found text of length {}  at url {}\nskipping" \
                         .format(self.name, len(res), url))
        else:
            self.logger.info("{} Scrap Bolt found with {} paragraphs at url {}"\
                         .format(self.name, len(res), url))
            for parag in res :
                self.emit([info, parag])
