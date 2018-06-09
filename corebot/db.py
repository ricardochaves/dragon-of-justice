import logging
import os
from datetime import datetime

from pymongo import MongoClient


class MongoCore:
    def __init__(self):
        self.mongo_client = MongoClient(os.environ.get("MONGO_URI"), int(os.environ.get("MONGO_PORT")))

        self.db = self.mongo_client[os.environ.get("MONGO_DB_NAME")]
        self.user_list_collection = self.db["userlist"]
        self.congressperson_collection = self.db["congressperson"]
        self.worker_collection = self.db["worker"]

    def insert_user(self, user_id):
        data = {"user_id": user_id, "following": []}
        return self.user_list_collection.update(self._build_user_key(user_id), data, upsert=True)

    def get_user_following(self, user_id):
        return self.user_list_collection.find_one(self._build_user_key(user_id))["following"]

    def add_congressperson_to_follow(self, user_id, congressperson_id):

        return self._execute_update("$addToSet", user_id, congressperson_id)

    def remove_congressperson_to_follow(self, user_id, congressperson_id):

        return self._execute_update("$pull", user_id, congressperson_id)

    def add_congressperson_to_list(self, name, application_id):
        key = {"application_id": application_id}
        data = {"application_id": application_id, "name": name}
        return self.congressperson_collection.update(key, data, upsert=True)

    def get_congressperson(self, id):
        return self.congressperson_collection.find_one({"application_id": id})

    def get_congressperson_name(self, id):
        logging.info("get_politico_name: id: %s", id)
        return self.get_congressperson(int(id))["name"]

    @staticmethod
    def _build_user_key(user_id):
        return {"user_id": user_id}

    def _execute_update(self, command, user_id, congressperson_id):

        value = {command: {"following": {"id": congressperson_id}}}

        self.user_list_collection.find_one_and_update(self._build_user_key(user_id), value)
        return self.get_congressperson_name(congressperson_id)

    def update_last_execution(self, dt):
        data = {"id": "1", "data": dt}
        return self.worker_collection.update({"id": "1"}, data, upsert=True)

    def get_last_execution(self):
        worker = self.worker_collection.find_one({"id": "1"})
        if not worker:
            self.update_last_execution(datetime.now())
            return datetime.now()

        return worker["data"]
