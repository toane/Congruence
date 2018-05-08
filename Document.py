class Document:
    def __init__(self, search_term, article_url, article_content, timestamp=0, weight=0, blob=None, url_hash=''):
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
        self.url_hash = url_hash
        self.weight = weight
        self.blob = blob


    @property
    def json_value(self):
        # return vars(self)
        return {"search_term": self.search_term, \
                "article_url": self.article_url,\
                "article_content":self.article_content,\
                "timestamp":self.timestamp, \
                "url_hash": self.url_hash,\
                "weight":self.weight,\
                "blob":self.blob
                }

