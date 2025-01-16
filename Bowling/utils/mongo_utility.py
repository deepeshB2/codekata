import pymongo
import os
import logging

logging.getLogger('pymongo').setLevel(logging.ERROR)


def get_mongo_client(mongoTable='jobQueue'):
    try:
        mongoDbClientURL = "mongodb+srv://root:4bevs4BrCF6AHDtE@cluster1.i8xr9.mongodb.net/bowling?retryWrites=true&w=majority"
        # print('mongo url: ', mongoDbClientURL)
        gMongoDbClient = pymongo.MongoClient(mongoDbClientURL)
        mydb = gMongoDbClient["bowling"]
        mydb = mydb[mongoTable]
        return mydb
    except Exception as e:
        logging.error(e, stack_info=True, exc_info=True)
        logging.debug('Catch block in get MongoClient')
        return None
