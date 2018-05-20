import os

from streamparse import Bolt
from libs.scrappers.DiplomatScrapper import get_search_result
from bolts.search.SearchBolt import SearchBolt

class DiploSearchBolt(SearchBolt):
    def initialize(self, conf, ctx):
        self.search_function = get_search_result
        self.name = "Diplo"
        super().initialize(conf, ctx)
        
