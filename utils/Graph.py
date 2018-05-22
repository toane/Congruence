
from itertools import chain, combinations, groupby
import utils.analyse as analyse
import utils.Wordcount_methods as wcm
import graphviz as gv
#import numpy as np
from typing import Dict
import math
import json

dot_node_colors = {
    "PERSON" : "blue",
    "ORGANIZATION" : "red",
    "TOPIC" : "green"
}

json_node_colors = {
    "PERSON" : "rgb( 0, 51, 102)",
    "ORGANIZATION" : "rgb(255, 204, 0)",
    "TOPIC" : "rgb( 204, 204, 204)"
}


class GlobalGraph:

    def __init__(self, wordcounts, \
                 n = 5, \
                 subjects = ["PERSON", "ORGANIZATION", "TOPIC"],
                 logger = None):
        
        def log(s):
            if logger:
                global logi
                logger.info(str(s))
                
        # wordcounts is a list of wordcount dictionaries
        # print("wordcounts for graph :", wordcounts)
        
        wordcounts_selected = list(map(
            lambda d: {k : d[k] for k in d.keys() if k in subjects},
            wordcounts))
        
        # print("selected : ", list(wordcounts_selected))
        # dictionnary with wordcount for each subject
        wordcount_dict = wcm.aggregate_wordcount_dicts(wordcounts_selected)
        # take the n firsts of each subject : these will be the nodes of the graph
        
        wordcount_dict_best = \
            { k : wcm.take_firsts(v, n=n) for k,v in wordcount_dict.items() }
        

        
        def item_in_wordcount(item, wc):
            wordcount_keys = map(lambda item: item[0], wc)
            return item[0] in wordcount_keys
        
            
        def select_if_in_global_best(wordcount_dic):
            return { k : [ item for item in v if item_in_wordcount(item, wordcount_dict_best[k])] \
                     for k, v in wordcount_dic.items()}
        

        # now we need to build the edges :
        # we select in the initial wordcounts the items that appear in wordcount_dict_best
        wordcounts_best = [select_if_in_global_best(article_wordcount) \
                                for article_wordcount in wordcounts_selected]
        
        #print("wordcounts_best : ", wordcounts_best)
        # we flatten the dictionnaries
        wordcounts_best_flattened = list(map(wcm.aggregate_subjects, wordcounts_best))
        
        nodes_lists = list(map( lambda l : list(map(lambda x:x[0],l)), wordcounts_best_flattened))

        #print("nodes lists : ", list(nodes_lists))
        
        # we build the edges by combining elements that appear in the same article
        # we have to sort by name first so that we can later aggregate edges
        nodes_lists_sorted = list(map(lambda l: sorted(l), nodes_lists))
        edges_lists = list(map( lambda wc : list(combinations(wc, 2)),
                                nodes_lists_sorted))


        # we flatten the list of edges : some edges will appear multiple times
        edges_multiples = list(chain.from_iterable(edges_lists))
        # we count edges
        edges_grouped = groupby(sorted(edges_multiples))
        # print("edges_grouped : ", list(edges_grouped))
        edges_weighted = list(map(lambda it : (it[0], len(list(it[1]))), edges_grouped))
        #print(edges_weighted)
        
        # we select the 50% best edges
        # weights = np.array(list(map(lambda x:x[1], edges_weighted)))
        # q2 = np.percentile(weights, 50)
        # edges_selected = filter(lambda x:x[1] >= q2, edges_weighted)
        
        
        self.nodes = wordcount_dict_best
        self.edges = list(edges_weighted)

        # print("nodes : {}".format(self.nodes))
        # print("edges : {}".format(self.edges))
        
    def to_dot(self):
        dot = gv.Graph()

        for subject in self.nodes.keys():
            for node in self.nodes[subject]:
                dot.node(node[0], **{"color" :dot_node_colors[subject], 
                                  "width" : str(math.sqrt(node[1])), 
                                  "fontsize" :  str(10*math.sqrt(node[1])), 
                                  "shape" : "circle"} )
        
        # for node in self.nodes:
        #     dot.node(node[0][0], **{"color" :dot_node_colors[node[0][1]], \
        #                             "width" : str(math.sqrt(node[1])), \
        #                             "fontsize" :  str(10*math.sqrt(node[1])), \
        #                             "shape" : "circle"} )

        # print("\nedges : ", self.edges, "\n")
        # print("\nedges_small ",  [(edge[0][0][0], edge[1][0][0]) for edge in self.edges], "\n")
        # print("\nedges_set ",  set([(edge[0][0][0], edge[1][0][0]) for edge in self.edges]), "\n")
            

        for edge in self.edges:
            dot.edge(edge[0][0], edge[0][1], **{"penwidth": str(edge[1])})

        dot.view()

    def to_json(self) -> str:
        """
        builds JSON str for vis.js graph data
        node=dict{id: 1, value: 5, label: 'Balkany' , color: 'rgb(237,28,36)'}
        :return:
        """
        json_output = ''
        class Node:
            def __init__(self, id, value, label, color, group=''):
                self.id = id
                self.value = value
                self.label = label
                self.color = color
                self.group = group

            def get_dict(self):
                return self.__dict__

        class Edge:
            def __init__(self, from_node, to_node, title, color, names_index):
                # recupere un id (ici position dans la liste node_names)
                self.from_node = names_index[from_node]
                self.to_node = names_index[to_node]
                self.title = title
                self.color = color

            def get_dict(self):
                vals = self.__dict__
                vals["from"] = vals.pop('from_node')
                vals["to"] = vals.pop('to_node')
                return vals

        json_nodes = []
        json_edges = []
        names_index = {}

        idx = 0
        for node_type, nodes_list in self.nodes.items():
            for node in nodes_list:
                # print(idx, node_type, node)
                node_name = node[0]
                node_value = node[1]
                color = json_node_colors[node_type]
                node = Node(idx, node_value, node_name,color, node_type)
                json_nodes.append(node)
                names_index[node_name] = idx
                idx += 1

        # print("index : ", names_index)
        
        for edge in self.edges:
            edge = Edge(edge[0][0], edge[0][1],edge[1],'rgb(100,100,100)', names_index)
            json_edges.append(edge)
            
        nodes_dec = [node.get_dict() for node in json_nodes] # liste de dicts
        edges_doc = [edge.get_dict() for edge in json_edges]
        # return json.dumps({"nodes": nodes_dec, "edges": edges_doc})
        return json.dumps({"nodes": nodes_dec, "edges": edges_doc})
