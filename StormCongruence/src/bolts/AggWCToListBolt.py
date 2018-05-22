
from streamparse import Bolt
import os

class AggWCToListBolt(Bolt):
    outputs = [
        Stream(fields =['info', 'wordcounts_list'], name="default"),
        Stream(fields =['info', 'keywords'], name="rec")]
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wcs = []
        self.count = 0
            
    def process(self, tup):
        info = tup.values[0]
        wordcount_dict = tup.values[1]
        
        self.wcs.append(wordcount_dict)

        if self.count = 10:
            global_wordcount = wcm.aggregate_wordcount_dicts(wordcounts)
            global_wordcount_dict_best = {k : wcm.take_firsts(v, n=3)
                                          for k,v in global_wordcount.items()
                                          if k in ["PERSON", "ORGANIZATION"]}
            global_wordcount_best = wcm.aggregate_subjects(global_wordcount_dict_best)
            for token in global_wordcount_best:
                self.emit([info, token[0]])
        self.emit([info, self.wcs])
