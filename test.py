#!/usr/bin/python3
import sys

from scrappers.CNNScrapper import CNNScrapper
from scrappers.FigaroScrapper import FigaroStaticScrapper
from scrappers.LiberationScrapper import LiberationStaticScrapper
from scrappers.NYTScrapper import NYTScrapper
from scrappers.NouvelobsScrapper import NouvelobsStaticScrapper

from DBFace import DBFace
from analyse import Analyser
from scrappers.BBCScrapper import BBCScrapper

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
        
        nys.start()
        bbs.start()
        cnn.start()
        
    # # twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    #
    # cnn.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = 'magic pony'
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])


    print("running search for keywords {}".format(keywords))
    run_scrappers(keywords, langs=['en', 'fr'])

    dbf = DBFace()
    analyser = Analyser('http://192.168.1.53',9000)
    fwst = dbf.find_with_search_term(keywords)
    print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', keywords))
    fwc = dbf.find_with_content(keywords)
    print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', keywords))
    notk = dbf.find_tokenifiable(langs=["fr","en"])
    print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() <= 1 else 's'))
    dbf.batch_tokenify(notk, analyser)

    fwst = dbf.find_with_search_term(keywords)
    fwc = dbf.find_with_content(keywords)

    initial_kw = [[keywords]]

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

    a = dbf.python_wordcount(keywords, "super")
    b = dbf.compute_global_wordcount(a)
    c = list(map(lambda wc : dbf.take_firsts(wc), b.values()))
    print(c)
