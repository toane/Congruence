#!/usr/bin/python3
import sys

from DBFace import DBFace
from analyse import Analyser
from scrappers.BBCScrapper import BBCScrapper
from scrappers.CNNScrapper import CNNScrapper
from scrappers.FigaroScrapper import FigaroStaticScrapper
from scrappers.LiberationScrapper import LiberationStaticScrapper
from scrappers.NYTScrapper import NYTScrapper
from scrappers.NouvelobsScrapper import NouvelobsStaticScrapper

import utils.Wordcount_methods as wcm
import view.Graph as graph
from scrappers.v1.DiplomatScrapper import DiplomatScrapper

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

    
    fwst = dbf.find_with_search_term(current_keywords)
    print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', keywords))
    
    fwc = dbf.find_with_content(keywords, exact=True)
    print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', keywords))
    
    notk = dbf.find_tokenifiable(langs=["en"])
    nowc = dbf.find_wordcountable(langs=["en"])
    print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() == 1 else 's'))
    print("found {} wordcountable doc{}".format(nowc.count(), '' if nowc.count() == 1 else 's'))
    dbf.batch_tokenify(notk, analyser)

    wordcounts = dbf.get_wordcounts(current_keywords)
    global_wordcount = wcm.global_wordcount(wordcounts)
    filtered_wordcounts = wcm.select_subjects(global_wordcount)
    wordcount_best =  list(map(wcm.aggregate_subjects, wordcount_dicts_best))
    for token in wordcount_best:
        recursive_search(initial_keywords, token[0][0], depth-1, langs)





if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = "kim jong"
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])

    print("running search for keywords {}".format(keywords))
    run_scrappers(keywords, langs=['en'])

    dbf = DBFace()
    analyser = Analyser('http://192.168.1.53', 9000)
    # analyser = Analyser('http://localhost', 9000)
    # print(analyser.annotate("TUMBLR"))

    fwst = dbf.find_with_search_term(keywords)
    print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', keywords))
    fwc = dbf.find_with_content(keywords, exact=True)
    print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', keywords))
    notk = dbf.find_tokenifiable(langs=["en"])
    nowc = dbf.find_wordcountable(langs=["en"])
    print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() == 1 else 's'))
    print("found {} wordcountable doc{}".format(nowc.count(), '' if nowc.count() == 1 else 's'))
    dbf.batch_tokenify(notk, analyser)
    # dbf.batch_wordcount(nowc, analyser)

    # tknifier = Analyser(host='http://localhost', port=9000)
    # txt = fwst[2].article_content
    # print("running analyzer on {}".format(txt))
    # r = tknifier.proper_nouns_extractor(txt)
    # print(r)
    # tknifier.quit()


    # max_depth = 4
    # depth = 1
    # while depth <= 4:
    #     for idx,art in enumerate(initial_kw):
    #         docs_a = dbf.find_with_content(keywords)
    #         docs_b = dbf.find_with_search_term(keywords)
    #         docs = docs_a + docs_b
    #         for d in docs:
    #             # recuperer noms presents dans le doc tels que fournis par le tokenizer
    #             # nouveau scrapping -> les noms sont dans la bdd
    #             # noms = tokenizer_liste_noms
    #
    #     max_depth = max_depth + 1
    #

    #print("running wordcount with mongo mapreduce")
    #dbf.mongo_wordcount(keywords, "super")

    
    wordcounts = dbf.get_wordcounts(keywords)
    global_wordcount = wcm.global_wordcount(wordcounts)
    filtered_wordcounts = wcm.select_subjects(global_wordcount)
    
    c = list(map(lambda wc: wcm.take_firsts(wc), filtered_wordcounts.values()))
    print(c)


    g = graph.GlobalGraph(wordcounts)
    g.to_dot()
