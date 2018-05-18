import os

from streamparse import Bolt

class ScrapBolt(Bolt):
    outputs = ['info', 'text']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
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
