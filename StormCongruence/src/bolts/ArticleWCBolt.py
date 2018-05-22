
from streamparse import Bolt
import os
import utils.Wordcount_methods as wcm

class ArticleWCBolt(Bolt):
    outputs = ['info', 'wordcounts_dict']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
            
    def process(self, tup):
        info = tup.values[0]
        tokens = tup.values[1]

        wordcount = wcm.wordcount(tokens)
        wordcount_dict = wcm.group_by_subject(wordcount)
        self.emit([info, wordcount_dict])
