import os

from streamparse import Bolt
from libs.scrappers.NYTScrapper import get_page_content
from bolts.scrap.ScrapBolt import ScrapBolt

class NYTScrapBolt(ScrapBolt):
    def initialize(self, conf, ctx):
        self.scrap_function = get_page_content
        self.name = "NYT"
        super().initialize(conf, ctx)
        
