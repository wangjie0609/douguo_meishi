import pymongo
from pymongo.collection import Collection


class Connect_mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port = 27017)
        self.db_data = self.client['douguo_meishi']

    def insert_item(self,item):

        db_collection = Collection(self.db_data,'douguo_meishi_item')
        db_collection.insert(item)

mongn_info = Connect_mongo()