
from streamparse import Bolt
import os

class AggWCToListBolt(Bolt):
    outputs = ['info', 'wordcounts_list']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.wcs = []
            
    def process(self, tup):
        info = tup.values[0]
        wordcount_dict = tup.values[1]
        
        self.wcs.append(wordcount_dict)

        self.emit([info, self.wcs])
