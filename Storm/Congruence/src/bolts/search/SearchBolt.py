import os

from streamparse import Bolt

class SearchBolt(Bolt):
    outputs = ['info', 'url']

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.searched = set()
        

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
