from pymongo import MongoClient, TEXT
from Document import Document
import hashlib
import codecs
import os
from pymongo.errors import ServerSelectionTimeoutError
from typing import List


class DBFace:

    def __init__(self):
        client = MongoClient('localhost', 27018)
        db = client.mdb
        self.coll = db.articol
        content_col="article_content"
        mongo_idx_name = '_'.join([content_col,"text"])
        if mongo_idx_name not in db.articol.index_information().keys():
            print("db: creating text index on article_content")
            db.articol.create_index([("article_content", TEXT)])

    def get_hash(self, url: str):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def write_file(self, url:str, content:str):
        if len(content) > 0:  # dont write empty strings
            with codecs.open(os.path.join("scrapped_data", self.get_hash(url) + '.txt').encode('utf-8'), 'w',
                             encoding='utf-8') as f:
                f.write(content)

    def build_doc(self, data):
        return Document(data['search_term'],
                        data['article_url'],
                        data['article_content'],
                        data['timestamp'],
                        data['weight'],
                        data['blob'],
                        data['url_hash'])

    def find_with_content(self, search_term: str) -> List[Document]:
        """
        returns Document containing search_term
        :param search_term:
        :return: list[Document]
        """
        present = []
        for doc in self.coll.find({"$text": {"$search": search_term}}):
            d = self.build_doc(doc)
            present.append(d)
        print("found {} document{} containing text {}".format(len(present),'' if len(present) <= 1 else 's',search_term))
        return present

    def find_with_search_term(self, search_term: str) -> List[Document]:
        """
        returns a list of Document where article_content contains search_term
        :param search_term:
        :return: list[Document]
        """
        present = []
        for doc in self.coll.find({"search_term": search_term}):
            d = self.build_doc(doc)
            present.append(d)
        print("found {} document{} originating from keyword {}".format(len(present), '' if len(present) <= 1 else 's', search_term))
        return present

    def add_record(self, search_terms: str, url: str, content: str) -> List[Document]:
        """
        Adds a Document to the db
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
            print("article length = 0 chars (failed scrapping ?), skipping".format(url))
        else:
            new_record = Document(search_terms, url, content, url_hash=url_hash)
            print('adding article {}, length {}'.format(url, len(content)))
            try:
                self.coll.insert_one(new_record.json_value)
            except ServerSelectionTimeoutError as sst:
                print(sst)