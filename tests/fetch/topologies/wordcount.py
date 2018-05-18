"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.scraper import ScrapBolt
from spouts.words import WordSpout


class WordCount(Topology):
    word_spout = WordSpout.spec()
    count_bolt = ScrapBolt.spec(inputs={word_spout: Grouping.fields('word')},
                                    par=2)
