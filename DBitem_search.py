class Search:
    def __init__(self,search_term, current_search_term, articles_ids, global_wordcount):
        """
        describe the result of a research
        :param search_term: the search term that initiated this research
        :param current_search_term : the search term that found the given articles
        :param articles_ids : the ids of the articles found by this research
        :param global_wordcount : the wordcount on all the articles
        """
        
        self.search_term = search_term
        self.current_search_term = current_search_term
        self.articles_ids = articles_ids
        self.global_wordcount = global_wordcount

    def json_values(self):
        return {"search_term" : self.search_term, \
                "current_search_term": self.current_search_term, \
                "articles_ids" : self.articles_ids, \
                "global_wordcount" : self.global_wordcount
                }
