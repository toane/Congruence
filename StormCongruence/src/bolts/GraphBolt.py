
import config.config as config
config.init()

from streamparse import Bolt
import os
from utils.Graph import GlobalGraph
from utils.DBFace import DBFace

class GraphBolt(Bolt):
    outputs = ['info', 'graph_json']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.db = DBFace()
        
    def process(self, tup):
        info = tup.values[0]
        wordcounts = tup.values[1]

        graph = GlobalGraph(wordcounts, logger = self.logger)
        graph_json = graph.to_json()
                                  
        self.db.insert_graph(graph_json, info["initial_keyword"])
        self.logger.info("graph inserted in db")
        
        self.emit([info, graph_json])
