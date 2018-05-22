
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
        
        self.logger.info("graphbolt received message")
        self.logger.info("graphbolt message : {}".format(tup.values))
        wordcounts = tup.values[1]

        graph = GlobalGraph(wordcounts, logger = self.logger)
        self.logger.info("graph initialized")
        graph_json = graph.to_json()
        self.logger.info("graph generated :{}".format(graph_json))
                          
        self.db.insert_graph(graph_json)
        self.logger.info("produced graph : {}".format(graph_json))
        
        #self.emit([info, graph_json])
