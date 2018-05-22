
from streamparse import Bolt
import os
import utils.Wordcount_methods as wc

class ArticleWCBolt(Bolt):
    outputs = ['info', 'wordcounts_dict']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
            
    def process(self, tup):
        info = tup.values[0]
        tokens_dict = tup.values[1]

        wordcount_dict = {
            subject : wc.wordcount(tokens) for subject, tokens in tokens_dict.items()
        }
        #self.logger.info("ArticleWordcount : {}".format(wordcount_dict))

        self.emit([info, wordcount_dict])
