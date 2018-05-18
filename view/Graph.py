
from itertools import chain, combinations, groupby
import utils.analyse as analyse
import utils.Wordcount_methods as wcm
import graphviz as gv
import numpy as np
from typing import Dict
import math
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
        
        # wordcount_best list of list, all the tokens from each article
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

        # wordcounts_dicts : list of dictionnaries
        wordcount_dicts = list(map(lambda wc: \
                                   wcm.select_subjects(wc,subjects = subjects),
                                   wordcounts))
        
        global_wordcount = wcm.global_wordcount(wordcounts)
        global_wordcount_aggregated = analyse.aggregate_proper_names_in_wordcount(global_wordcount)
        global_wordcount_dict = wcm.select_subjects(global_wordcount_aggregated, \
                                                    subjects = subjects)
        global_wordcount_dict_best = \
            { k : wcm.take_firsts(v, n=n) for k,v in global_wordcount_dict.items() }

        def item_in_wordcount(item, wordcount):
            wordcount_keys = map(lambda item: item[0], wordcount)
            return item[0] in wordcount_keys
            
        def select_if_in_global_best(wordcount_dic):
            return { k : [ item for item in v if item_in_wordcount(item, global_wordcount_dict_best[k])] \
                     for k, v in wordcount_dic.items() }

        wordcount_dicts_best = [select_if_in_global_best(article_wordcount) \
                                for article_wordcount in wordcount_dicts]
        
        wordcount_best = list(map(wcm.aggregate_subjects, wordcount_dicts_best))

        print(wordcount_best)
        
        self.nodes = list(chain.from_iterable(wordcount_best))
        self.edges = list(chain.from_iterable( \
                                 map(lambda wc : list(combinations(wc, 2)), wordcount_best)))

    def to_dot(self):
        dot = gv.Graph()

        for node in self.nodes:
            dot.node(node[0][0], **{"color" :dot_node_colors[node[0][1]], \
                                    "width" : str(math.sqrt(node[1])), \
                                    "fontsize" :  str(10*math.sqrt(node[1])), \
                                    "shape" : "circle"} )

        # print("\nedges : ", self.edges, "\n")
        # print("\nedges_small ",  [(edge[0][0][0], edge[1][0][0]) for edge in self.edges], "\n")
        # print("\nedges_set ",  set([(edge[0][0][0], edge[1][0][0]) for edge in self.edges]), "\n")
            
        graph_edges_multiple = sorted([(edge[0][0][0], edge[1][0][0]) for edge in self.edges])
        graph_edges_grouped = groupby(graph_edges_multiple)
        graph_edges_weighted = list(map(lambda it : (it[0], len(list(it[1]))), graph_edges_grouped))

        weights = np.array(list(map(lambda x:x[1], graph_edges_weighted)))
        q1 = np.percentile(weights, 25)
        q2 = np.percentile(weights, 50)
        
        print(graph_edges_weighted)
        for edge in graph_edges_weighted:
            # print("edge : ", edge)
            if edge[1] >= q2:

                dot.edge(edge[0][0], edge[0][1], **{"penwidth": str(edge[1])})

        dot.view()

    def to_json(self) -> Dict:
        """
        builds JSON for vis.js graph data
        node=dict{id: 1, value: 5, label: 'Balkany' , color: 'rgb(237,28,36)'}
        :return:
        """
        json_output = ''
        class Node:
            def __init__(self, id, value, label, color):
                self.id=id
                self.value=value
                self.label=label
                self.color=color

            def get_json(self):
                ret = []
                for k, v in self.__dict__.items():
                    ret.append("{}:'{}'".format(k, v))
                return '{'+','.join(ret)+'}'

        class Edge:
            def __init__(self, from_node, to_node, title, color):
                # recupere un id (ici position dans la liste node_names)
                self.from_node = node_names.index(from_node)
                self.to_node = node_names.index(to_node)
                self.title = title
                self.color = color

            def get_json(self):
                ret = []
                for k, v in self.__dict__.items():
                    if k == "from_node": k = "from"
                    if k == "to_node": k = "to"
                    ret.append("{}:'{}'".format(k, v))
                return '{'+','.join(ret)+'}'

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
            node = Node(idx, 1, node_name,color)
            json_nodes.append(node)

        for edge in graph_edges_weighted:
            # if edge[1] >= q2:
            # print('edge value', edge[1])
            # print("{} -> {} ".format(edge[0][0], edge[0][1]))
            edge = Edge(edge[0][0], edge[0][1],1,'rgb(100,100,100')
            json_edges.append(edge)

        nodes_dec = "nodes = [{}]".format(','.join([node.get_json() for node in json_nodes]))
        edges_doc="edges = [{}]".format(','.join([edge.get_json() for edge in json_edges]))
        return {"nodes": nodes_dec, "edges": edges_doc}
