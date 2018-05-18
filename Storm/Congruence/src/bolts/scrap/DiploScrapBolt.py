import os

from streamparse import Bolt
from libs.scrappers.DiplomatScrapper import get_page_content
from bolts.scrap.ScrapBolt import ScrapBolt

class DiploScrapBolt(ScrapBolt):
    def initialize(self, conf, ctx):
        self.scrap_function = get_page_content
        self.name = "Diplo"
        super().initialize(conf, ctx)
        
