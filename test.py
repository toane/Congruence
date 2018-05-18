#!/usr/bin/python3
import sys

from scrappers.CNNScrapper import CNNScrapper
from scrappers.FigaroScrapper import FigaroStaticScrapper
from scrappers.LiberationScrapper import LiberationStaticScrapper
from scrappers.NYTScrapper import NYTScrapper
from scrappers.NouvelobsScrapper import NouvelobsStaticScrapper

from DBFace import DBFace
from analyse import Analyser
import analyse
from scrappers.BBCScrapper import BBCScrapper
from scrappers.DiplomatScrapper import DiplomatScrapper

import utils.Wordcount_methods as wcm

import view.Graph as graph

"""
1) lancer les scrappers sur un mot cle
2) ils cherchent des articles et les ajoutent à la bdd si ceux-ci n'existent pas avec une url identique
3) effectuer le calcul a partir d'une requete sur la base
"""

threads=[]
def thread_accumulator(thread):
    # print("started thread {}".format(thread))
    threads.append(thread)

def run_scrappers(keywords, langs=['en']):

    if 'fr' in langs:
        ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords, thread_accumulator)
        ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords, thread_accumulator)
        fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords, thread_accumulator)
        
        ls.start()
        ns.start()
        fs.start()
        

    if 'en' in langs:
        nys = NYTScrapper("https://www.nytimes.com/search/", keywords, thread_accumulator)
        bbs = BBCScrapper("https://www.bbc.co.uk/search?", keywords, thread_accumulator)
        cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords, thread_accumulator)
        dps = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keywords, thread_accumulator)
        
        nys.start()
        bbs.start()
        cnn.start()
        dps.start()
        
    # # twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    #
    # cnn.start()
    for t in threads:
        t.join()


def recursive_search(initial_keywords, current_keywords, depth, langs = ['en']):
    if depth == 0:
        return None
        
    dbf = DBFace()
    analyser = Analyser('http://192.168.1.53', 9000)

    print("running recursive search at depth {} for keyword {} from initial keyword {}".format(depth, current_keywords, initial_keywords))
    run_scrappers(current_keywords, langs=['en'])

    
    fwst = dbf.find_with_search_term(current_keywords)
    print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', current_keywords))
    
    fwc = dbf.find_with_content(keywords, exact=True)
    print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', current_keywords))
    
    notk = dbf.find_tokenifiable(langs=["en"])
    nowc = dbf.find_wordcountable(langs=["en"])
    print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() == 1 else 's'))
    print("found {} wordcountable doc{}".format(nowc.count(), '' if nowc.count() == 1 else 's'))
    dbf.batch_tokenify(notk, analyser)

    wordcounts = dbf.get_wordcounts(current_keywords)
    global_wordcount = wcm.global_wordcount(wordcounts)
    global_wordcount_dict = wcm.select_subjects(global_wordcount, \
                                                subjects = ["PERSON", "ORGANIZATION"])

    print(global_wordcount_dict)
    
    global_wordcount_dict_best = {k : wcm.take_firsts(v, n=3) for k,v in global_wordcount_dict.items()}
    global_wordcount_best = wcm.aggregate_subjects(global_wordcount_dict_best)
    for token in global_wordcount_best:
        recursive_search(initial_keywords, token[0][0], depth-1, langs)





if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = "kim jong"
    
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])

    recursive_search(keywords, keywords, 1, langs = ['en'])
    
    dbf = DBFace()
    
    wordcounts = dbf.get_wordcounts(keywords)
    global_wordcount = wcm.global_wordcount(wordcounts)
    global_wordcount_aggregated = analyse.aggregate_proper_names_in_wordcount(global_wordcount)
    filtered_wordcounts = wcm.select_subjects(global_wordcount_aggregated)
    
    c = list(map(lambda wc: wcm.take_firsts(wc, n=3), filtered_wordcounts.values()))
    #print(c)


    g = graph.GlobalGraph(wordcounts, n=6)
    g.to_dot()
