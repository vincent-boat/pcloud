from pymongo import MongoClient

class DBB():
    c = MongoClient()

    @staticmethod
    def connect()   :
        DBB.c = MongoClient("mongodb://localhost:27017/")


