import os
import logging
from pymongo import MongoClient


class MongoCore:
    def __init__(self):
        self.mongo_client = MongoClient(
            os.environ.get("MONGO_URI"), int(os.environ.get("MONGO_PORT"))
        )

        self.db = self.mongo_client[os.environ.get('MONGO_DB_NAME')]
        self.user_list_collection = self.db['userlist']
        self.congressperson_collection = self.db['congressperson']

    def insert_user(self, user_id):
        key = {
            "user_id": user_id
        }
        data = {
            "user_id": user_id,
            "following": []
        }
        return self.user_list_collection.update(key, data, upsert=True)

    def get_user_following(self, user_id):
        return self.user_list_collection.find_one({
            "user_id": user_id
        })['following']

    def add_congressperson_to_follow(self, user_id, congressperson_id):
        key = {
            "user_id": user_id
        }
        value = {
            "$addToSet": {
                "following": {
                    "id": congressperson_id
                }
            }
        }
        self.user_list_collection.find_one_and_update(key, value)
        return self.get_congressperson_name(congressperson_id)

    def remove_congressperson_to_follow(self, user_id, congressperson_id):
        key = {
            "user_id": user_id
        }
        value = {
            "$pull": {
                "following": {
                    "id": congressperson_id
                }
            }
        }
        self.user_list_collection.find_one_and_update(key, value)
        return self.get_congressperson_name(congressperson_id)

    def add_congressperson_to_list(self, name, application_id):
        key = {
            "application_id": application_id
        }
        data = {
            "application_id": application_id,
            "name": name
        }
        return self.congressperson_collection.update(key, data, upsert=True)

    def get_congressperson(self, id):
        return self.congressperson_collection.find_one({"application_id": id})

    def get_congressperson_name(self, id):
        logging.info('get_politico_name: id: %s', id)
        return self.get_congressperson(int(id))['name']
