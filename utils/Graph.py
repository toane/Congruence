
from itertools import chain, combinations, groupby
import utils.analyse as analyse
import utils.Wordcount_methods as wcm
import graphviz as gv
import numpy as np
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

class ArticlesGraph:
    
    def __init__(self, wordcounts):
        """ 
        ArticlesGraph: selects the five first tokens from each article for each subject,
        then add edges between tokens if they appear in the same article
        Problem : all 15 tokens from each article are related to each other, 
        and the graph is thus clumsy
        
        params:
        :wordcounts : list of wordcounts (complete wordcount for each article)
        """
        
        # wordcounts_dicts : list of dictionnaries
        wordcount_dicts = list(map(wcm.select_subjects, wordcounts))
        
        # print("\nwordcounts : ", self.wordcounts, "\n")

        # wordcount_dicts_best : list of dictionnaries, 5 items per subject
        wordcount_dicts_best = list(map( \
                                 lambda dic : {k: wcm.take_firsts(v) for k,v in dic.items() }, \
                                         wordcount_dicts))
        # print("\n wordcount_dicts_best : ", list(wordcount_dicts_best), "\n")
        
        # nodes_lists list of list, all the tokens from each article
        wordcount_best =  list(map(wcm.aggregate_subjects, wordcount_dicts_best))
        # print("\n wordcount_best : ", wordcount_best, "\n")
        
        
        
        self.nodes = list(chain.from_iterable(wordcount_best))
        self.edges = list(chain.from_iterable( \
                                 map(lambda wc : list(combinations(wc, 2)), wordcount_best)))

        # print("edges : ", list(self.edges))
    
    def to_dot(self):
        dot = gv.Graph()

        for node in self.nodes:
            dot.attr("node", color=dot_node_colors[node[0][1]])
            dot.node(node[0][0])

        for edge in self.edges:
            # print("edge : ", edge)

            dot.edge(edge[0][0][0], edge[1][0][0])

        dot.view()


class GlobalGraph:

    def __init__(self, wordcounts, \
                 n = 5, \
                 subjects = ["PERSON", "ORGANIZATION", "TOPIC"]):

        # wordcounts is a list of wordcount dictionaries

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
        print("wordcounts_best : ", wordcounts_best)
        # we flatten the dictionnaries
        wordcounts_best_flattened = list(map(wcm.aggregate_subjects, wordcounts_best))
        nodes_lists = list(map( lambda l : list(map(lambda x:x[0],l)), wordcounts_best_flattened))

        print("nodes lists : ", list(nodes_lists))
        
        # we build the edges by combining elements that appear in the same article
        edges_lists = list(map( lambda wc : list(combinations(wc, 2)),
                                nodes_lists))


        # we flatten the list of edges : some edges will appear multiple times
        edges_multiples = list(chain.from_iterable(edges_lists))
        # we count edges
        edges_grouped = groupby(sorted(edges_multiples))
        # print("edges_grouped : ", list(edges_grouped))
        edges_weighted = list(map(lambda it : (it[0], len(list(it[1]))), edges_grouped))
        print(edges_weighted)
        # we select the 50% best edges
        weights = np.array(list(map(lambda x:x[1], edges_weighted)))
        q2 = np.percentile(weights, 75)
        edges_selected = filter(lambda x:x[1] >= q2, edges_weighted)
        
        
        self.nodes = wordcount_dict_best
        self.edges = list(edges_selected)

        print("nodes : ", self.nodes)
        print("edges : ", self.edges)
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
            def __init__(self, from_node, to_node, title, color):
                # recupere un id (ici position dans la liste node_names)
                self.from_node = node_names.index(from_node)
                self.to_node = node_names.index(to_node)
                self.title = title
                self.color = color

            def get_dict(self):
                vals = self.__dict__
                vals["from"] = vals.pop('from_node')
                vals["to"] = vals.pop('to_node')
                return vals

        graph_edges = set([(edge[0][0][0], edge[1][0][0]) for edge in self.edges])

        node_names = list(set(node[0][0] for node in self.nodes))

        json_nodes = []
        json_edges = []
        node_name_type = dict()

        graph_edges_multiple = sorted([(edge[0][0][0], edge[1][0][0]) for edge in self.edges])
        graph_edges_grouped = groupby(graph_edges_multiple)
        graph_edges_weighted = list(map(lambda it : (it[0], len(list(it[1]))), graph_edges_grouped))

        # construction d'un dict nom_de_la_node: type{person/orga/topic}
        for node in self.nodes:
            node_type = node[0][1]
            node_name = node[0][0]
            node_name_type[node_name] = node_type

        for idx, node_name in enumerate(node_names):
            node_type = node_name_type[node_name]
            color = json_node_colors[node_type]
            node = Node(idx, 1, node_name,color, node_type)
            json_nodes.append(node)

        for edge in graph_edges_weighted:
            # if edge[1] >= q2:
            # print('edge value', edge[1])
            # print("{} -> {} ".format(edge[0][0], edge[0][1]))
            edge = Edge(edge[0][0], edge[0][1],1,'rgb(100,100,100)')
            json_edges.append(edge)

        nodes_dec = [node.get_dict() for node in json_nodes] # liste de dicts
        edges_doc = [edge.get_dict() for edge in json_edges]
        # return json.dumps({"nodes": nodes_dec, "edges": edges_doc})
        return json.dumps({"nodes": nodes_dec, "edges": edges_doc})
