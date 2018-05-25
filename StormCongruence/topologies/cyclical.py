
import config.config as config
config.init()

from streamparse.thrift import GlobalStreamId

from streamparse import Grouping, Topology
from spouts.ListenerSpout import ListenerSpout

from bolts.SearchBolt import SearchBolt
from bolts.ScrapBolt import ScrapBolt


from bolts.NLP.SentenceSplitBolt import SentenceSplitBolt as SSplitBolt
from bolts.NLP.TokenizeBolt import TokenizeBolt

from bolts.ArticleWCBolt import ArticleWCBolt
from bolts.WCAggregatorBolt import WCAggregatorBolt
from bolts.GraphBolt import GraphBolt
from bolts.RecursiveBolt import RecursiveBolt

keyword_rec = GlobalStreamId(componentId='wc_agg_bolt', streamId='rec')
class WordCount(Topology):
    config = {
        "ui.host" : "http://localhost"
        }

    
    socket_listener_spout = ListenerSpout.spec()
    
    # diplo_search_bolt = \
    #     OmniSearchBolt.spec( \
    #                     inputs=[socket_listener_spout], par=1 , \
    #                     config = {"OmniSearchBoltName" : "Diplo"} )

    rec_bolt = RecursiveBolt.spec(
        inputs=[socket_listener_spout, keyword_rec], par=1)

    bbc_search_bolt = SearchBolt.spec(
        inputs=[rec_bolt], par=1, 
        config = {"OmniSearchBoltName" : "BBC"} )
    
    nyt_search_bolt = SearchBolt.spec(
        inputs=[rec_bolt], par=1,
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
    
    wc_agg_bolt = WCAggregatorBolt.spec(
        inputs = [article_wc_bolt], par = 1)

    graph_bolt = GraphBolt.spec(
        inputs = [wc_agg_bolt], par = 1)
    
