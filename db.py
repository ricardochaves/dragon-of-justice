import os
import logging
from pymongo import MongoClient

mongo_client = MongoClient(
    os.environ.get("MONGO_URI"), int(os.environ.get("MONGO_PORT"))
)

db = mongo_client[os.environ.get('MONGO_DB_NAME')]

COLLECTION = 'seguindo'
POLITICO_COLLECTION = 'politicos'


def get_db():
    return db[COLLECTION]


def get_politico_db():
    return db[POLITICO_COLLECTION]


def insert(telegran_id):
    key = {
        "telegran_id": telegran_id
    }
    data = {
        "telegran_id": telegran_id,
        "seguindo": []
    }
    get_db().update(key, data, upsert=True)


def getOne(telegran_id):
    return get_db().find_one({
        "telegran_id": telegran_id
    })['seguindo']


def addOne(telegran_id, politico_id):
    key = {
        "telegran_id": telegran_id
    }
    get_db().find_one_and_update(key, {"$addToSet": {"seguindo": {"id": politico_id}}})


def removeOne(telegran_id, politico_id):
    key = {
        "telegran_id": telegran_id
    }
    get_db().find_one_and_update(key, {"$pull": {"seguindo": {"id": politico_id}}})


def add_politico(name, application_id):
    key = {
        "application_id": application_id
    }
    data = {
        "application_id": application_id,
        "name": name
    }
    get_politico_db().update(key, data, upsert=True)


def get_politico(id):
    return get_politico_db().find_one({"application_id": id})


def get_politico_name(id):
    logging.info('get_politico_name: id: %s', id)
    return get_politico(int(id))['name']
