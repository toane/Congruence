import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# max_pool_size : nb max de connections à la base
# a priori pas besoin d'y toucher
# client = MongoClient('localhost', 27017, maxPoolSize=1000)


# récupère une db (même si elle n'existe pas)
db = client.testdb

# récupère la collection d'une db
coll = db.testcoll

# liste les collections
#     db.collection_names(include_system_collections=False)
# (les collections dans lesquelles on n'a rien inséré n'apparaissent pas


# insère dans une collection : il faut insérer un dictionnaire (on peut aussi insérer des trucs plus exotiques)
coll.insert_one({"hello" : "world"})

# find_one : retourne une valeur de la collection
# coll.find_one()
