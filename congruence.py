#!/usr/bin/python3
import sys

scrappers_version = 1

if scrappers_version == 1:
    from scrappers.CNNScrapper import CNNScrapper
    from scrappers.FigaroScrapper import FigaroStaticScrapper
    from scrappers.LiberationScrapper import LiberationStaticScrapper
    from scrappers.NYTScrapper import NYTScrapper
    from scrappers.NouvelobsScrapper import NouvelobsStaticScrapper
    from scrappers.BBCScrapper import BBCScrapper
    from scrappers.DiplomatScrapper import DiplomatScrapper
else:
    from scrappers.v2.CNNScrapper import CNNScrapper
    from scrappers.v2.FigaroScrapper import FigaroStaticScrapper
    from scrappers.v2.LiberationScrapper import LiberationStaticScrapper
    from scrappers.v2.NYTScrapper import NYTScrapper
    from scrappers.v2.NouvelobsScrapper import NouvelobsStaticScrapper
    from scrappers.v2.BBCScrapper import BBCScrapper
    from scrappers.v2.DiplomatScrapper import DiplomatScrapper
    
from utils.DBFace import DBFace
from utils.analyse import Analyser
import utils.analyse as analyse

import utils.Wordcount_methods as wcm

import utils.Graph as graph


class Congruence:

    def __init__(self):
        self.threads = []
        self.keywords = ''
        self.dbf = DBFace()

    def run(self, keywords):
        self.keywords = keywords
        self.recursive_search(self.keywords, self.keywords, 1, langs = ['en'])
        wordcounts = self.dbf.get_wordcounts(self.keywords)
        global_wordcount = wcm.global_wordcount(wordcounts)
        global_wordcount_aggregated = analyse.aggregate_proper_names_in_wordcount(global_wordcount)
        filtered_wordcounts = wcm.select_subjects(global_wordcount_aggregated)
        c = list(map(lambda wc: wcm.take_firsts(wc, n=3), filtered_wordcounts.values()))
        self.g = graph.GlobalGraph(wordcounts, n=6)
        return self.g.to_json()

    def thread_accumulator(self,thread):
        # print("started thread {}".format(thread))
        self.threads.append(thread)

    def run_scrappers(self,keywords, langs=['en']):

        if 'fr' in langs:
            if scrappers_version == 1:
                ns = NouvelobsStaticScrapper("https://recherche.nouvelobs.com/?", keywords, self.thread_accumulator)
                ls = LiberationStaticScrapper("http://www.liberation.fr/recherche/?", keywords, self.thread_accumulator)
                fs = FigaroStaticScrapper("http://recherche.lefigaro.fr/recherche/", keywords, self.thread_accumulator)
            else:
                ns = NouvelobsStaticScrapper(keywords, requested_by= self.thread_accumulator)
                ls = LiberationStaticScrapper(keywords, requested_by= self.thread_accumulator)
                fs = FigaroStaticScrapper(keywords, requested_by= self.thread_accumulator)

            ls.start()
            ns.start()
            fs.start()


        if 'en' in langs:
            if scrappers_version == 1:
                nys = NYTScrapper("https://www.nytimes.com/search/", keywords, self.thread_accumulator)
                bbs = BBCScrapper("https://www.bbc.co.uk/search?", keywords, self.thread_accumulator)
                # cnn = CNNScrapper("https://edition.cnn.com/search/?", keywords, self.thread_accumulator)
                dps = DiplomatScrapper('https://www.googleapis.com/customsearch/v1element?', keywords, self.thread_accumulator)
            else:
                nys = NYTScrapper(keywords, requested_by=self.thread_accumulator)
                bbs = BBCScrapper(keywords, requested_by=self.thread_accumulator)
                # cnn = CNNScrapper(keywords, self.thread_accumulator)
                dps = DiplomatScrapper(keywords, requested_by=self.thread_accumulator)
            
            nys.start()
            bbs.start()
            # cnn.start()
            dps.start()

        for t in self.threads:
            t.join()

    def recursive_search(self, initial_keywords, current_keywords, depth, langs = ['en']):
        if depth == 0:
            return None

        # analyser = Analyser('http://192.168.1.53', 9000)
        analyser = Analyser('http://localhost', 9000)

        print("running recursive search at depth {} for keyword {} from initial keyword {}".format(depth, current_keywords, initial_keywords))
        self.run_scrappers(current_keywords, langs=['en'])

        fwst = self.dbf.find_with_search_term(current_keywords)
        print("found {} document{} originating from keyword {}".format(len(fwst), '' if len(fwst) <= 1 else 's', current_keywords))

        fwc = self.dbf.find_with_content(self.keywords, exact=True)
        print("found {} document{} containing text {}".format(len(fwc), '' if len(fwc) <= 1 else 's', current_keywords))

        notk = self.dbf.find_tokenifiable(langs=["en"])
        nowc = self.dbf.find_wordcountable(langs=["en"])
        print("found {} tokenifiable doc{}".format(notk.count(), '' if notk.count() == 1 else 's'))
        print("found {} wordcountable doc{}".format(nowc.count(), '' if nowc.count() == 1 else 's'))
        self.dbf.batch_tokenify(notk, analyser)

        wordcounts = self.dbf.get_wordcounts(current_keywords)
        global_wordcount = wcm.global_wordcount(wordcounts)
        global_wordcount_dict = wcm.select_subjects(global_wordcount, \
                                                    subjects = ["PERSON", "ORGANIZATION"])

        print(global_wordcount_dict)

        global_wordcount_dict_best = {k : wcm.take_firsts(v, n=3) for k,v in global_wordcount_dict.items()}
        global_wordcount_best = wcm.aggregate_subjects(global_wordcount_dict_best)
        for token in global_wordcount_best:
            self.recursive_search(initial_keywords, token[0][0], depth-1, langs)

    if __name__ == '__main__':
        print("running on Python version {}".format(sys.version))


