"""
Word count topology
"""

from streamparse import Grouping, Topology
from spouts.ListenerSpout import ListenerSpout

from bolts.OmniSearchBolt import OmniSearchBolt
from bolts.search.DiploSearchBolt import DiploSearchBolt
from bolts.scrap.DiploScrapBolt import DiploScrapBolt

from bolts.search.BBCSearchBolt import BBCSearchBolt
from bolts.scrap.BBCScrapBolt import BBCScrapBolt

from bolts.search.NYTSearchBolt import NYTSearchBolt
from bolts.scrap.NYTScrapBolt import NYTScrapBolt

from bolts.NLP.SentenceSplitBolt import SentenceSplitBolt as SSplitBolt

class WordCount(Topology):

    socket_listener_spout = ListenerSpout.spec()
    
    diplo_search_bolt = \
        OmniSearchBolt.spec( \
                        inputs=[socket_listener_spout], par=1 , \
                        config = {"OmniSearchBoltName" : "Diplo"} )
    
    diplo_scrap_bolt = DiploScrapBolt.spec(inputs=[diplo_search_bolt], par=5)
    
    #bbc_search_bolt = BBCSearchBolt.spec(inputs=[socket_listener_spout], par=1)
    #bbc_scrap_bolt = BBCScrapBolt.spec(inputs=[bbc_search_bolt], par=5)

    #nyt_search_bolt = NYTSearchBolt.spec(inputs=[socket_listener_spout], par=1)
    #nyt_scrap_bolt = NYTScrapBolt.spec(inputs=[nyt_search_bolt], par=5)

    ssplit_bolt = SSplitBolt.spec(inputs=[diplo_scrap_bolt], \
                par=1, \
                config={"CoreNLPHost":"http://localhost",\
                        "CoreNLPPort":9000})
