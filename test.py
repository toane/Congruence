#!/usr/bin/python3

import config.config as conf 
conf.init(USE_STORM_ = False,
          RECURSIVE_DEPTH_ = 1)

from congruence import Congruence



import sys
from utils.DBFace import DBFace
import utils.Wordcount_methods as wcm
import utils.Graph as graph

if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = "kim jong"
    
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])


    congruence = Congruence()
    congruence.recursive_search(keywords, keywords, conf.RECURSIVE_DEPTH, langs = ['en'])
    
    dbf = DBFace()

    wordcounts = dbf.get_wordcounts(keywords)
    global_wordcount = wcm.aggregate_wordcount_dicts(wordcounts)

    # print(global_wordcount)


    g = graph.GlobalGraph(wordcounts, n=6)
    #print(g.to_json())
    g.to_dot()
    
