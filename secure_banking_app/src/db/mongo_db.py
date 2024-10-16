from pymongo import MongoClient

def get_mongo_client():
    return MongoClient('mongodb://localhost:27017/')
