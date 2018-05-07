#!/usr/bin/python3
from LiberationScrapper import LiberationStaticScrapper
from NouvelobsScrapper import NouvelobsStaticScrapper
from FigaroScrapper import FigaroStaticScrapper
from CNNScrapper import CNNScrapper
import sys
if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = "antisemite"
    # https://recherche.nouvelobs.com/?referer=nouvelobs&q=khadafi
    ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords)
    ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords)
    fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords)
    cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords)
    # ls.start()
    # ns.start()
    fs.start()
    cnn.start()
    # ls.join()