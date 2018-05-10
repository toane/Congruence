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
from stanfordNLP.analyse import Analyser

"""
1) lancer les scrappers sur un mot cle
2) ils cherchent des articles et les ajoutent à la bdd si ceux-ci n'existent pas avec une url identique
3) effectuer le calcul a partir d'une requete sur la base
"""


def run_scrappers(keywords):
    ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords)
    nys = NYTScrapper("https://www.nytimes.com/search/", keywords)
    bbs = BBCScrapper("https://www.bbc.co.uk/search?", keywords)
    ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords)
    fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords)
    cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords)
    # # twentymin = VingtMinutesScrapper("https://www.20minutes.fr/search?", keywords)
    #
    bbs.start()
    nys.start()
    # ls.start()
    # ns.start()
    # fs.start()
    cnn.start()
    # ls.join()
    # ns.join()
    # fs.join()
    bbs.join()
    nys.join()
    cnn.join()


if __name__ == '__main__':
    print("running on Python version {}".format(sys.version))
    keywords = 'confident'
    # si argument fourni en ligne de commande
    if len(sys.argv) > 1:
        keywords = ' '.join(sys.argv[1:])

    run_scrappers(keywords)

    dbf = DBFace()
    fwst = dbf.find_with_search_term(keywords)
    print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', keywords))
    fwc = dbf.find_with_content(keywords)
    print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', keywords))
    notk = dbf.find_tokenifiable()
    print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() <= 1 else 's'))
    dbf.batch_tokenify(notk)
    # print(notk.next().keys())


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