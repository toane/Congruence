#!/usr/bin/python3
from LiberationScrapper import LiberationStaticScrapper
from VingtMinutesScrapper import VingtMinutesScrapper
from NouvelobsScrapper import NouvelobsStaticScrapper
from FigaroScrapper import FigaroStaticScrapper
from CNNScrapper import CNNScrapper
from NYTScrapper import NYTScrapper
from BBCScrapper import BBCScrapper
from DBFace import DBFace
import sys

"""
1) lancer les scrappers sur un mot cle
2) ils cherchent des articles et les ajoutent à la bdd si ceux-ci n'existent pas avec une url identique
3) effectuer le calcul a partir d'une requete sur la base
"""

if __name__ == '__main__':

    keywords = 'petoncle'
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])

    print("running on Python version {}".format(sys.version))

    dbf = DBFace()
    fwst = dbf.find_with_search_term(keywords)
    fwc = dbf.find_with_content(keywords)

    ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords)
    nys = NYTScrapper("https://www.nytimes.com/search/", keywords)
    bbs = BBCScrapper("https://www.bbc.co.uk/search?", keywords)
    ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords)
    fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords)
    # cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords)
    # # twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    #
    bbs.start()
    nys.start()
    ls.start()
    ns.start()
    fs.start()
    # cnn.start()
    # twentymin.start()
    # ls.join()
    # ns.join()
    # fs.join()
    bbs.join()
    nys.join()
    # twentymin.join()

    fwst = dbf.find_with_search_term(keywords)
    fwc = dbf.find_with_content(keywords)

    initial_kw = [[keywords]]
    max_depth = 4
    depth = 1
    while depth <= 4:
        for idx,art in enumerate(initial_kw):
            docs_a = dbf.find_with_content(keywords)
            docs_b = dbf.find_with_search_term(keywords)
            docs = docs_a + docs_b
            for d in docs:
                # recuperer noms presents dans le doc tels que fournis par le tokenizer
                # nouveau scrapping -> les noms sont dans la bdd
                # noms = tokenizer_liste_noms

        max_depth = max_depth + 1





