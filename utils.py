from pymongo import MongoClient
from StorageModel import StorageModel
import hashlib
import codecs
import os
from pymongo.errors import ServerSelectionTimeoutError


def get_hash(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def write_file(url, content):
    if len(content) > 0:  # dont write empty strings
        with codecs.open(os.path.join("scrapped_data", get_hash(url) + '.txt').encode('utf-8'), 'w',
                         encoding='utf-8') as f:
            f.write(content)


def add_record(search_terms, url, content):
    url_hash=get_hash(url)
    new_record = StorageModel(search_terms, url, content, url_hash=url_hash)
    print('adding article {}, length {}'.format(url, len(content)))
    # print(new_record.mongo_value)
    try:
        client = MongoClient('localhost', 27018)
        db = client.mdb
        coll = db.articol
        # coll.insert_one(new_record.mongo_value)
        coll.insert_one({"piss":"hitler","charniere":"papierpeint"})
    except ServerSelectionTimeoutError as sst:
        print(sst)