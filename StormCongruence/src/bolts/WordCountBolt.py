
from streamparse import Bolt
import os


class WordCountBolt(Bolt):
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wc = {}
        

        
    def add_one(self, token):
        if token in self.wc:
            self.wc[token] += 1
        else:
            self.wc[token] = 1
            
    def process(self, tup):
        info = tup.values[0]
        tokens = tup.values[1]

        for token in tokens:
            self.add_one(token)

        self.emit([info, list(self.wc.items())])
