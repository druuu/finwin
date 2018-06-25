from pymongo import MongoClient
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

database_name = 'ynotebook'
DB = MongoClient("mongodb://%s:%s@127.0.0.1:27017/%s" % ('root', quote_plus('#SMXN5NQb5xWvkPg7@'), database_name), connect=False)[database_name]

