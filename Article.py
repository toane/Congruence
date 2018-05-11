class Article:
    def __init__(self, search_term, article_url, article_content, lang='', current_search_term='',
                 wordcount=None,tokenified=None,timestamp=0, weight=0, blob=None, url_hash='', mongo_id=None):
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
        self.current_search_term = current_search_term
        self.tokenified = tokenified
        self.timestamp = timestamp
        self.url_hash = url_hash
        self.wordcount = wordcount
        self.weight = weight
        self.blob = blob
        self.lang = lang
        self.mongo_id = mongo_id

    @property
    def json_value(self):
        # return vars(self)
        return {"search_term": self.search_term, \
                "article_url": self.article_url,\
                "article_content": self.article_content,\
                "tokenified": self.tokenified,\
                "wordcount": self.wordcount,\
                "current_search_term": self.current_search_term,\
                "lang": self.lang,\
                "timestamp": self.timestamp, \
                "url_hash": self.url_hash,\
                "weight": self.weight,\
                "blob": self.blob,
                "mongo_id": self.mongo_id
                }

