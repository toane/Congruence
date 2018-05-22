
from streamparse import Bolt
import os
import utils.Wordcount_methods as wc

class AggregateWCBolt(Bolt):
    outputs = ['info', 'wordcounts_dict']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wc = {}
            
    def process(self, tup):
        info = tup.values[0]
        tokens_dict = tup.values[1]

        wordcount_dict = {
            subject : wc.wordcount(tokens) for subject, tokens in tokens_dict.items()
        }
        

        self.emit([info, wordcount_dict])
