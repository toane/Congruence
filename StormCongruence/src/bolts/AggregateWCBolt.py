
from streamparse import Bolt
import os
import utils.Wordcount_methods as wc

class AggregateWCBolt(Bolt):
    outputs = ['info', 'global_wordcount']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wc = {}
            
    def process(self, tup):
        info = tup.values[0]
        wordcounts_dict = tup.values[1]
        
        self.wc = wc.global_wordcount([wordcounts_dict, self.wc])

        self.emit([info, self.wc])
