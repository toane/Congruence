
from streamparse import Bolt
import os
from utils.Graph import GlobalGraph
from utils.DBFace import DBFace
import json

class GraphBolt(Bolt):
    outputs = ['info', 'graph_json']
    
    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.db = DBFace()
        
    def process(self, tup):
        
        self.logger.info("graphbolt received message")
        self.logger.info("graphbolt message : {}".format(tup.values))
        info = tup.values[0]
        wordcounts = tup.values[1]

        graph = GlobalGraph(wordcounts, from_dicts = True)
        graph_json = graph.to_json()
        self.logger.info("graph generated :{}".format(graph_json))
                          
        self.db.insert_graph(graph_json)
        self.logger.info("produced graph : {}".format(graph_json))
        
        #self.emit([info, graph_json])
