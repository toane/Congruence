from libs.analyse import Analyser
import os
from streamparse import Bolt

class SentenceSplitBolt(Bolt):
    outputs = ['info', 'sentence']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        #self.logger.info("initialised sentenceSplitBolt with conf : {}".format(conf))
        self.host = conf["CoreNLPHost"]
        self.port = conf["CoreNLPPort"]
        self.analyser = Analyser(self.host, self.port)
        
    def process(self, tup):
        
        info = tup.values[0]
        text = tup.values[1]
        sentences = self.analyser.advanced_sentences_split(text)
        self.logger.info("found {} sentences in text {}".format(len(list(sentences)), text))
        for sentence in sentences:
            self.emit([info, sentence])
