"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.scraper import ScrapBolt
from spouts.listener import ListenSpout


class WordCount(Topology):
    word_spout = ListenSpout.spec()
    count_bolt = ScrapBolt.spec(inputs={word_spout: Grouping.fields('word')},
                                    par=2)
