
from itertools import chain, combinations

import utils.Wordcount_methods as wcm
import graphviz as gv

node_colors = {
    "PERSON" : "blue",
    "ORGANIZATION" : "red",
    "TOPIC" : "green"
}

class Graph:
    
    def __init__(self, wordcounts):


        # wordcounts_dicts : list of dictionnaries
        wordcount_dicts = list(map(wcm.select_subjects, wordcounts))
        
        # print("\nwordcounts : ", self.wordcounts, "\n")

        # wordcount_dicts_best : list of dictionnaries, 5 items per subject
        wordcount_dicts_best = list(map( \
                                 lambda dic : {k: wcm.take_firsts(v) for k,v in dic.items() }, \
                                         wordcount_dicts))
        
        print("\n wordcount_dicts_best : ", list(wordcount_dicts_best), "\n")
        

        # wordcount_best list of list, all the tokens from each article
        wordcount_best =  list(map(wcm.aggregate_subjects, wordcount_dicts_best))
        
        print("\n wordcount_best : ", wordcount_best, "\n")

        self.nodes = chain.from_iterable(wordcount_best)
        self.edges = list(chain.from_iterable( \
                                 map(lambda wc : list(combinations(wc, 2)), wordcount_best)))

        # print("edges : ", list(self.edges))


    
    def to_dot(self):
        dot = gv.Graph()

        for node in self.nodes:
            dot.attr("node", color=node_colors[node[0][1]])
            dot.node(node[0][0])

        
        for edge in self.edges:
            # print("edge : ", edge)

            dot.edge(edge[0][0][0], edge[1][0][0])

        dot.view()
