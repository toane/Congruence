import os

from streamparse import Bolt
from libs.scrappers.BBCScrapper import get_search_result
from bolts.search.SearchBolt import SearchBolt


class BBCSearchBolt(SearchBolt):
    def initialize(self, conf, ctx):
        self.search_function = get_search_result
        self.name = "BBC"
        super().initialize(conf, ctx)
