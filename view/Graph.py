

from utils.Wordcount_methods import Wordcount_methods

class Graph:
    def __init__(self, wordcounts):
        self.wordcounts = map(lambda wc : sort(wc, key= lambda item : - item[1]), wordcounts)

        self.
