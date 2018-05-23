"""
Word count topology
"""


from streamparse import Grouping, Topology
from spouts.ListenerSpout import ListenerSpout

from bolts.SearchBolt import SearchBolt
from bolts.ScrapBolt import ScrapBolt


from bolts.NLP.SentenceSplitBolt import SentenceSplitBolt as SSplitBolt
from bolts.NLP.TokenizeBolt import TokenizeBolt

from bolts.ArticleWCBolt import ArticleWCBolt
from bolts.WCAggregatorBolt import WCAggregatorBolt
from bolts.GraphBolt import GraphBolt


class WordCount(Topology):

    socket_listener_spout = ListenerSpout.spec()
    
    # diplo_search_bolt = \
    #     OmniSearchBolt.spec( \
    #                     inputs=[socket_listener_spout], par=1 , \
    #                     config = {"OmniSearchBoltName" : "Diplo"} )
    

    bbc_search_bolt = SearchBolt.spec(
        inputs=[socket_listener_spout], par=1, 
        config = {"OmniSearchBoltName" : "BBC"} )
    
    nyt_search_bolt = SearchBolt.spec(
        inputs=[socket_listener_spout], par=1,
        config = {"OmniSearchBoltName" : "NYT"} )
                        


    bbc_scrap_bolt = ScrapBolt.spec(
        inputs=[bbc_search_bolt], par = 1,
        config = {"OmniScrapBoltName": "BBC"})
    
    nyt_scrap_bolt = ScrapBolt.spec(
        inputs=[nyt_search_bolt], par = 1,
        config = {"OmniScrapBoltName": "NYT"})
    
    # ssplit_bolt = SSplitBolt.spec( 
    #     inputs=[bbc_scrap_bolt, nyt_scrap_bolt], par=1,
    #     config={"CoreNLPHost":"http://localhost",
    #             "CoreNLPPort":9000})

    tokenize_bolt = TokenizeBolt.spec(
        inputs = [bbc_scrap_bolt, nyt_scrap_bolt], par=1,
        config={"CoreNLPHost":"http://localhost",
                "CoreNLPPort":9000})

    # person_wc_bolt = WordCountBolt.spec(
    #     inputs = [tokenize_bolt["person"]], par=1)

    article_wc_bolt = ArticleWCBolt.spec(
        inputs = [tokenize_bolt], par = 1)
    
    agg_wc_to_list_bolt = WCAggregatorBolt.spec(
        inputs = [article_wc_bolt], par = 1)

    graph_bolt = GraphBolt.spec(
        inputs = [agg_wc_to_list_bolt], par = 1)
    
