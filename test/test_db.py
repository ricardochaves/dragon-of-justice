import sys
import unittest
from datetime import datetime
from test.helper import cleardb

from corebot.db import MongoCore
from freezegun import freeze_time

sys.path.append("..")


class TestDb(unittest.TestCase):
    def setUp(self):
        cleardb()

    def test_instance_db_mongo(self):
        """
            Test: Integration: DB: New:Test constructor
        """

        mongo = MongoCore()
        self.assertIsInstance(mongo, MongoCore)

    def test_insert_user(self):
        """
            Test: Integration: DB: insert_user: Must enter new user
        """

        mongo = MongoCore()
        inserted = mongo.insert_user(123)
        recupered = mongo.user_list_collection.find({"user_id": 123})

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered.count(), 1)
        self.assertEqual(recupered[0]["following"], [])

    def test_get_user_following(self):
        """
            Test: Integration: DB: user_following: Must return to the follow list
        """

        mongo = MongoCore()
        mongo.add_congressperson_to_list("fulano", 456)
        mongo.add_congressperson_to_list("fulano2", 789)

        mongo.insert_user(123)
        name_1 = mongo.add_congressperson_to_follow(123, 456)
        name_2 = mongo.add_congressperson_to_follow(123, 789)

        following = mongo.get_user_following(123)

        self.assertIsNotNone(following)
        self.assertIsInstance(following, list)
        self.assertEqual(len(following), 2)
        self.assertEqual(name_1, "fulano")
        self.assertEqual(name_2, "fulano2")

    def test_remove_congressperson_to_follow(self):
        """
            Test: Integration: DB: remove_congressperson_to_follow: Must remove from list
        """

        mongo = MongoCore()
        mongo.add_congressperson_to_list("fulano", 456)
        mongo.add_congressperson_to_list("fulano2", 789)

        mongo.insert_user(123)
        name_1 = mongo.add_congressperson_to_follow(123, 456)
        name_2 = mongo.add_congressperson_to_follow(123, 789)

        name_3 = mongo.remove_congressperson_to_follow(123, 456)

        following = mongo.get_user_following(123)

        self.assertIsNotNone(following)
        self.assertIsInstance(following, list)
        self.assertEqual(len(following), 1)
        self.assertEqual(name_1, "fulano")
        self.assertEqual(name_2, "fulano2")
        self.assertEqual(name_3, "fulano")

    def test_add_congressperson_to_list(self):
        """
            Test: Integration: DB: remove_congressperson_to_follow: Must add from list
        """

        mongo = MongoCore()

        inserted = mongo.add_congressperson_to_list("fulano", 123)

        recupered = mongo.congressperson_collection.find({"application_id": 123})

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered.count(), 1)

    def test_get_congressperson_name(self):
        """
            Test: Integration: DB: get_congressperson_name: Should return the name
        """
        mongo = MongoCore()

        inserted = mongo.add_congressperson_to_list("fulano", 123)

        recupered = mongo.get_congressperson_name(123)

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered, "fulano")

    @freeze_time("2018-06-21 01:11:56")
    def test_get_last_execution_first_time(self):
        """
            Test: Integration: DB: get_last_execution: Should insert datetime.now
        """
        mongo = MongoCore()

        last_execution = mongo.get_last_execution()
        result = mongo.worker_collection.find_one({"id": "1"})

        self.assertEqual(last_execution, datetime.now())
        self.assertEqual(result["data"], datetime.now())

    def test_get_last_execution_get_previews_inserted(self):
        """
            Test: Integration: DB: get_last_execution: Should get previews inserted datetime.now
        """

        mongo = MongoCore()

        with freeze_time("2019-01-04 01:11:56"):
            data = datetime.now()
            mongo.update_last_execution(data)

        last_execution = mongo.get_last_execution()

        self.assertEqual(last_execution, data)
        self.assertNotEquals(data, datetime.now())

    @freeze_time("2018-06-21 01:11:56")
    def test_update_last_execution(self):
        """
            Test: Integration: DB: update_last_execution: Should insert datetime.now
        """
        mongo = MongoCore()

        data = datetime.now()
        mongo.update_last_execution(data)

        result = mongo.worker_collection.find_one({"id": "1"})

        self.assertEqual(result["data"], data)

    @freeze_time("2018-06-21 01:11:56")
    def test_update_last_execution_previews_inserted(self):
        """
            Test: Integration: DB: update_last_execution: Should update previews inserted
        """
        mongo = MongoCore()

        data = datetime.now()
        mongo.update_last_execution(data)

        with freeze_time("2019-01-04 01:11:56"):
            data = datetime.now()
            mongo.update_last_execution(data)

        result = mongo.worker_collection.find_one({"id": "1"})

        self.assertEqual(result["data"], data)
