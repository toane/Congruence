import os

from streamparse import Bolt
from libs.scrappers.BBCScrapper import get_page_content
from bolts.scrap.ScrapBolt import ScrapBolt

class BBCScrapBolt(ScrapBolt):
    def initialize(self, conf, ctx):
        self.scrap_function = get_page_content
        self.name = "BBC"
        super().initialize(conf, ctx)
        
