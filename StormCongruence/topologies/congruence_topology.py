"""
Word count topology
"""

print("congruence 0")
from streamparse import Grouping, Topology
print("congruence 0")
from spouts.ListenerSpout import ListenerSpout
print("congruence 0")

from bolts.OmniSearchBolt import OmniSearchBolt
print("congruence 0")

#from bolts.scrap.DiploScrapBolt import DiploScrapBolt
#from bolts.scrap.BBCScrapBolt import BBCScrapBolt
#from bolts.scrap.NYTScrapBolt import NYTScrapBolt

from bolts.NLP.SentenceSplitBolt import SentenceSplitBolt as SSplitBolt
print("congruence 0")

class WordCount(Topology):

    socket_listener_spout = ListenerSpout.spec()
    
    diplo_search_bolt = \
        OmniSearchBolt.spec( \
                        inputs=[socket_listener_spout], par=1 , \
                        config = {"OmniSearchBoltName" : "Diplo"} )
    
    #diplo_scrap_bolt = DiploScrapBolt.spec(inputs=[diplo_search_bolt], par=5)
    
    #bbc_search_bolt = BBCSearchBolt.spec(inputs=[socket_listener_spout], par=1)
    #bbc_scrap_bolt = BBCScrapBolt.spec(inputs=[bbc_search_bolt], par=5)

    #nyt_search_bolt = NYTSearchBolt.spec(inputs=[socket_listener_spout], par=1)
    #nyt_scrap_bolt = NYTScrapBolt.spec(inputs=[nyt_search_bolt], par=5)

    # ssplit_bolt = SSplitBolt.spec(inputs=[diplo_scrap_bolt], \
    #             par=1, \
    #             config={"CoreNLPHost":"http://localhost",\
    #                     "CoreNLPPort":9000})
