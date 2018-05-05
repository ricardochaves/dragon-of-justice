import sys
sys.path.append("..")

import os
import unittest
from unittest import mock
from corebot.db import MongoCore
from test.helper import cleardb


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
        recupered = mongo.user_list_collection.find({
            "user_id": 123
        })

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered.count(), 1)
        self.assertEqual(recupered[0]['following'], [])

    def test_get_user_following(self):
        """
            Test: Integration: DB: user_following: Must return to the follow list
        """

        mongo = MongoCore()
        mongo.add_congressperson_to_list('fulano', 456)
        mongo.add_congressperson_to_list('fulano2', 789)

        mongo.insert_user(123)
        name_1 = mongo.add_congressperson_to_follow(123, 456)
        name_2 = mongo.add_congressperson_to_follow(123, 789)

        following = mongo.get_user_following(123)

        self.assertIsNotNone(following)
        self.assertIsInstance(following, list)
        self.assertEqual(len(following), 2)
        self.assertEqual(name_1, 'fulano')
        self.assertEqual(name_2, 'fulano2')

    def test_remove_congressperson_to_follow(self):
        """
            Test: Integration: DB: remove_congressperson_to_follow: Must remove from list
        """

        mongo = MongoCore()
        mongo.add_congressperson_to_list('fulano', 456)
        mongo.add_congressperson_to_list('fulano2', 789)

        mongo.insert_user(123)
        name_1 = mongo.add_congressperson_to_follow(123, 456)
        name_2 = mongo.add_congressperson_to_follow(123, 789)

        name_3 = mongo.remove_congressperson_to_follow(123, 456)

        following = mongo.get_user_following(123)

        self.assertIsNotNone(following)
        self.assertIsInstance(following, list)
        self.assertEqual(len(following), 1)
        self.assertEqual(name_1, 'fulano')
        self.assertEqual(name_2, 'fulano2')
        self.assertEqual(name_3, 'fulano')

    def test_add_congressperson_to_list(self):
        """
            Test: Integration: DB: remove_congressperson_to_follow: Must add from list
        """

        mongo = MongoCore()

        inserted = mongo.add_congressperson_to_list('fulano', 123)

        recupered = mongo.congressperson_collection.find({"application_id": 123})

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered.count(), 1)

    def test_get_congressperson_name(self):
        """
            Test: Integration: DB: get_congressperson_name: Should return the name 
        """
        mongo = MongoCore()

        inserted = mongo.add_congressperson_to_list('fulano', 123)

        recupered = mongo.get_congressperson_name(123)

        self.assertIsInstance(inserted, dict)
        self.assertIsNotNone(recupered)
        self.assertEqual(recupered, 'fulano')
