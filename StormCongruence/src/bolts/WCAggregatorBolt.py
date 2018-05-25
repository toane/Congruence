
from streamparse import Bolt, Stream
import os
import utils.Wordcount_methods as wcm
class WCAggregatorBolt(Bolt):
    outputs = [
        Stream(fields =['info', 'wordcounts_list'], name="default"),
        Stream(fields =['info', 'keywords'], name="rec")]
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wcs = {}
        self.count = 0
            
    def process(self, tup):
        info = tup.values[0]
        wordcount_dict = tup.values[1]

        # add received wordcount to the list of wordcounts
        kw = info["initial_keyword"]
        if kw in self.wcs:
            self.wcs[kw].append(wordcount_dict)
        else:
            self.wcs[kw] = [wordcount_dict]
            
        # emit the list of wordcounts associated with the
        # current keyword to the GraphBolt
        self.emit([info, self.wcs[kw]])
        
        # recursive call :
        # if the number of received wordcounts for the
        # keyword is a multiple of 10, send best token selection
        # as new keywords
        if len(self.wsc[kw]) % 10 == 0:
            global_wordcount = wcm.aggregate_wordcount_dicts(self.wcs[kw])
            global_wordcount_dict_best = {k : wcm.take_firsts(v, n=3)
                                          for k,v in global_wordcount.items()
                                          if k in ["PERSON", "ORGANIZATION"]}
            global_wordcount_best = wcm.aggregate_subjects(global_wordcount_dict_best)
            self.logger.info("sending tokens to RecursiveBolt")
            for token in global_wordcount_best:
                self.emit([info, token[0]], stream="rec")

    
