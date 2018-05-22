#!/usr/bin/python3
import sys

from utils.DBFace import DBFace
from utils.analyse import Analyser
import utils.Wordcount_methods as wcm
import utils.Graph as graph



scrappers_version = 2

if scrappers_version == 1:
    from scrappers.v1.CNNScrapper import CNNScrapper
    from scrappers.v1.FigaroScrapper import FigaroStaticScrapper
    from scrappers.v1.LiberationScrapper import LiberationStaticScrapper
    from scrappers.v1.NYTScrapper import NYTScrapper
    from scrappers.v1.NouvelobsScrapper import NouvelobsStaticScrapper
    from scrappers.v1.BBCScrapper import BBCScrapper
    from scrappers.v1.DiplomatScrapper import DiplomatScrapper
else:
    from scrappers.v2.CNNScrapper import CNNScrapper
    from scrappers.v2.FigaroScrapper import FigaroStaticScrapper
    from scrappers.v2.LiberationScrapper import LiberationStaticScrapper
    from scrappers.v2.NYTScrapper import NYTScrapper
    from scrappers.v2.NouvelobsScrapper import NouvelobsStaticScrapper
    from scrappers.v2.BBCScrapper import BBCScrapper
    from scrappers.v2.DiplomatScrapper import DiplomatScrapper
    from scrappers.v2.TheInterceptScrapper import TheInterceptScrapper
    
    


"""
1) lancer les scrappers sur un mot cle
2) ils cherchent des articles et les ajoutent à la bdd si ceux-ci n'existent pas avec une url identique
3) effectuer le calcul a partir d'une requete sur la base
"""

threads=[]
def thread_accumulator(thread):
    # print("started thread {}".format(thread))
    threads.append(thread)

def run_scrappers(keywords, langs):
    
    if 'fr' in langs:
        if scrappers_version == 1:
            ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords, thread_accumulator)
            ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords, thread_accumulator)
            fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords, thread_accumulator)
        else:
            ns = NouvelobsStaticScrapper(keywords, requested_by= thread_accumulator)
            ls = LiberationStaticScrapper(keywords, requested_by= thread_accumulator)
            fs = FigaroStaticScrapper(keywords, requested_by= thread_accumulator)
        ls.start()
        ns.start()
        fs.start()
        
    if 'en' in langs:
        if scrappers_version == 1:
            nys = NYTScrapper("https://www.nytimes.com/search/", keywords, thread_accumulator)
            bbs = BBCScrapper("https://www.bbc.co.uk/search?", keywords, thread_accumulator)
            # cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords, self.thread_accumulator)
            dps = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keywords, thread_accumulator)
        else:
            nys = NYTScrapper(keywords, requested_by=thread_accumulator)
            bbs = BBCScrapper(keywords, requested_by=thread_accumulator)
            # cnn = CNNScrapper(keywords, self.thread_accumulator)
            dps = DiplomatScrapper(keywords, requested_by=thread_accumulator)
            tis = TheInterceptScrapper(keywords, requested_by=thread_accumulator)
            
        nys.start()
        bbs.start()
        #cnn.start()
        dps.start()
        tis.start()
    # # twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    #
    # cnn.start()
    for t in threads:
        t.join()


def recursive_search(initial_keywords, current_keywords, depth, langs = ['en']):
    if depth == 0:
        return None
        
    dbf = DBFace()
    # analyser = Analyser('http://192.168.1.53', 9000)
    analyser = Analyser('http://localhost', 9000)

    print("running recursive search at depth {} for keyword {} from initial keyword {}".format(depth, current_keywords, initial_keywords))
    run_scrappers(current_keywords, langs)

    
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

    global_wordcount = wcm.aggregate_wordcount_dicts(wordcounts)
    print(global_wordcount)
    

    global_wordcount_dict_best = {k : wcm.take_firsts(v, n=3)
                                  for k,v in global_wordcount.items()
                                  if k in ["PERSON", "ORGANIZATION"]}
    global_wordcount_best = wcm.aggregate_subjects(global_wordcount_dict_best)

    print("global_wordcount_best :", global_wordcount_best)
    for token in global_wordcount_best:
        recursive_search(initial_keywords, token[0][0], depth-1, langs)





if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = "kim jong"
    
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])

    recursive_search(keywords, keywords, 2, langs = ['en'])
    
    dbf = DBFace()
    
    wordcounts = dbf.get_wordcounts(keywords)
    global_wordcount = wcm.aggregate_wordcount_dicts(wordcounts)

    print(global_wordcount)


    g = graph.GlobalGraph(wordcounts, n=6)
    #print(g.to_json())
    g.to_dot()
    
