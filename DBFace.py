from random import randrange

from pymongo import MongoClient, TEXT, ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError
from bson.code import Code

from Singleton import Singleton
from Article import Article
import hashlib
import codecs
import os
from typing import List, Dict

from analyse import Analyser


class DBFace(metaclass=Singleton):

    def __init__(self):
        print("new DBFace instance {}".format(id(self)))
        try:
            client = MongoClient("mongodb://localhost", 27017, serverSelectionTimeoutMS=5000)
            db = client.mdb
            self.coll = db.articol
            content_col = "article_content"
            mongo_idx_name = '_'.join([content_col,"text"])
            if mongo_idx_name not in db.articol.index_information().keys():
                print("db: creating text index on article_content")
                db.articol.create_index([("article_content", TEXT)])
        except ServerSelectionTimeoutError as sste:
            print("pymongo couldn't connect to mongodb server")

    def get_hash(self, url: str):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def do_nothing(self, func):
        pass

    def write_file(self, url: str, content: str):
        """
        writes content to a file with the url's hash as filename
        :param url:
        :param content:
        :return:
        """
        if len(content) > 0:  # dont write empty strings
            with codecs.open(os.path.join("scrapped_data", self.get_hash(url) + '.txt').encode('utf-8'), 'w',
                             encoding='utf-8') as f:
                f.write(content)

    def build_doc(self, data):
        return Article(search_term=data['search_term'],
                       current_search_term=data['current_search_term'],
                       article_url=data['article_url'],
                       article_content=data['article_content'],
                       lang=data['lang'],
                       timestamp=data['timestamp'],
                       weight=data['weight'],
                       blob=data['blob'],
                       url_hash=data['url_hash'],
                       wordcount=data['wordcount'],
                       tokenified = data['tokenified'],
                       mongo_id=data['_id'])

    def find_with_content(self, search_term: str, exact=False) -> List[Article]:
        """
        returns Document containing search_term
        :param search_term:
        :param exact: if true searches for exact string
        :return: list[Document]
        """
        if exact:
            search_term = "\"" + search_term + "\""
        return [self.build_doc(d) for d in self.coll.find({"$text": {"$search": search_term}})]

    def find_with_search_term(self, search_term: str) -> List[Article]:
        """
        returns a list of Document where article_content contains search_term
        :param search_term:
        :return: list[Document]
        """
        return [self.build_doc(d) for d in self.coll.find({"search_term": search_term})]

    def find_tokenifiable(self) -> List[Dict]:
        """
        returns a list of records with an empty tokenified field
        :return:
        """
        return self.coll.find({"tokenified": None})

    def batch_tokenify(self, records: Dict, analyser: Analyser):
        """
        runs content tokenization for all records
        :param records:
        :return:
        """
        n = records.count()
        print("computing tokenization for {} document{}".format(n, '' if n <=1 else 's'))
        for r in records:
            print('running tokenizer on {} (keyword {})'.format(r['article_url'], r['search_term']))
            tknis = analyser.get_tokens(r['article_content'])
            tknis_wc = analyser.tokencount(tknis)
            
            self.update_field(r['_id'], tknis,'tokenified')
            self.update_field(r['_id'], tknis_wc, 'wordcount')
            
    def update_field(self,_id, value: '', field: str='tokenified'):
        """
        updates field with value on record matching _id
        :param _id:
        :param field:
        :param value:
        :return:updated record
        """
        d = self.coll.find_one_and_update(
            {'_id': _id},
            {'$set': {field: value}},
            return_document=ReturnDocument.AFTER
        )
        return d

    def add_record(self, search_terms: str, url: str, content: str, lang: str='') -> List[Article]:
        """
        Adds a Document to the db
        :param lang:
        :param search_terms:
        :param url:
        :param content:
        :return:
        """

        url_hash = self.get_hash(url)

        # check if article is already archived
        if self.coll.find({"url_hash": url_hash}).count() > 0:
            print("article {} already present in db, skipping".format(url))
        elif len(content) == 0:
            print("scraped text length = 0 for {}, skipping".format(url))
        else:
            new_record = Article(search_terms, url, content, url_hash=url_hash, lang=lang)
            print('adding article {}, length {}'.format(url, len(content)))
            try:
                self.coll.insert_one(new_record.json_value)
            except ServerSelectionTimeoutError as sst:
                print(sst)


    def python_wordcount(self, search_term : str, result_collection : str):
        docs = self.coll.find({"search_term": search_term})
        wordcounts = [doc['wordcount'] for doc in docs]
        

        
    def mongo_wordcount(self, search_term : str, result_collection : str):
        mapper = Code(
            """
            function() { 
            for (var i = 0; i < this.wordcount.length; i++)  
            { emit(this.wordcount[i][0], this.wordcount[i][1][1]);} 
            }
            """)
        
        reducer = Code(
            """
            function(key, values) { 
            var count = 0; 
            values.forEach( function(v) {count += v}); 
            return count; 
            }
            """)

        params = {
            "query" : {"search_term" : search_term},
            "out" : {
                "replace" : result_collection
                }
        }

        self.coll.map_reduce(mapper, reducer, out=result_collection)
            
    

    ##### mongo db commands
    
    # # # # # brouillon wordcound
    #
    # var map = function() { for (var i = 0; i < this.wordcount.length; i++)  { emit(this.wordcount[i][0], this.wordcount[i][1][1]);} }
    # var reduce = function(key, values) { var count = 0; values.forEach( function(v) {count += v}); return count; }
    #
    # ## affiche le résultat
    # db.articol.mapReduce(map, reduce,  {out: {inline : true} })
    # ## enregistre le résultat dans la collection wordcount (un document par mot, c'est pas tip-top)
    # db.articol.mapReduce(map, reduce,  {out: "wordcount" })
    
