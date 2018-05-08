#!/usr/bin/python3
from LiberationScrapper import LiberationStaticScrapper
from NouvelobsScrapper import NouvelobsStaticScrapper
from FigaroScrapper import FigaroStaticScrapper
from CNNScrapper import CNNScrapper
from DBFace import DBFace
import sys

from VingtMinutesScrapper import VingtMinutesScrapper
"""
1) lancer les scrappers sur un mot cle
2) ils cherchent des articles et les ajoutent à la bdd si ceux-ci n'existent pas avec une url identique
3) effectuer le calcul a partir d'une requete sur la base
"""
if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))

    dbf = DBFace()
    keywords = "kig ha farz"
    fwst = dbf.find_with_search_term(keywords)
    fwc = dbf.find_with_content(keywords)
    ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords)
    ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords)
    fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords)
    cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords)
    twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    ls.start()
    ns.start()
    fs.start()
    ls.join()
    ns.join()
    fs.join()

    fwst = dbf.find_with_search_term(keywords)
    fwc = dbf.find_with_content(keywords)

    # cnn.start()  #
    # twentymin.start()
