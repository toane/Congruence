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


class ScrapBolt(Bolt):
    """
    takes in a url, and returns a list of paragraphs
    """
    
    outputs = ['info', 'parags']
    

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
        parags = self.scrap_function(url)

        if len(parags) == 0:
            self.logger.info( \
                "{} Scrap Bolt found text of length {}  at url {}\nskipping" \
                         .format(self.name, len(parags), url))
        else:
            self.logger.info("{} Scrap Bolt found with {} paragraphs at url {}"\
                         .format(self.name, len(parags), url))

            # if we emit each paragraph individually
            # we won't be able to build the links between
            # the article tokens, so we emit a list of paragraphs
            self.emit([info, parags])
