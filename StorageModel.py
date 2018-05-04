class StorageModel:
    def __init__(self, search_term, article_url, article_content, timestamp=0, weight=0, blob=None):
        """
        Describes a record
        :param search_term: the search term
        :param article_url: the article url
        :param timestamp:
        :param weight:
        :param blob: non specific binary data ( dict{'descriptor':value}
        """
        self.search_term = search_term
        self.article_url = article_url
        self.article_content = article_content
        self.timestamp = timestamp
        self.weight = weight
        self.blob = blob

    @property
    def mongo_value(self):
        return vars(self)
        # return {"search_term": self.search_term, \
        #         "article_url": self.article_url,\
        #         "article_content":self.article_content,\
        #         "timestamp":self.timestamp,\
        #         "weight":self.weight,\
        #         "blob":self.blob
        #         }

