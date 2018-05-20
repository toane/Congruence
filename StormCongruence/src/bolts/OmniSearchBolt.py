import os

from streamparse import Bolt

# from libs.scrappers.BBCScrapper import get_search_result as BBC_search_result
# from libs.scrappers.DiplomatScrapper import get_search_result as Diplo_search_result
# from libs.scrappers.NYTScrapper import  get_search_result as NYT_search_result

from ..scrappers.BBCScrapper import BBCScrapper
from ..scrappers.NYTScrapper import NYTScrapper
from ..scrappers.DiploScrapper import DiploScrapper

from ..scrappers.StaticScrapper import StaticScrapper.fetch as fetch

search_functions = {
    "BBC" :  BBC_parse_search,
    "NYT" : NYT_parse_search,
    "Diplo" : Diplo_parse_search
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
