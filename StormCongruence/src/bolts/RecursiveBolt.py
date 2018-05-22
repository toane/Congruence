
from streamparse import Bolt
import os

class RecursiveBolt(Bolt):
    outputs = ['info', 'keyword']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
            
    def process(self, tup):
        info = tup.values[0]

        if info["rec_n"] > 0:
            new_keyword = tup.values[1]
            info["keyword"] = new_keyword
            info["rec_n"] -= 1
            self.emit([info, new_keyword])
