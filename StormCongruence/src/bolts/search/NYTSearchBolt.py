import os

from streamparse import Bolt
from libs.scrappers.NYTScrapper import  get_search_result
from bolts.search.SearchBolt import SearchBolt



class NYTSearchBolt(SearchBolt):
    def initialize(self, conf, ctx):
        self.search_function = get_search_result
        self.name = "NYT"
        super().initialize(conf, ctx)
