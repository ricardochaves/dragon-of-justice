import os
import requests
import itertools
import logging

from urllib.parse import quote

from corebot.db import MongoCore


class Requester:

    def __init__(self, db=None):

        self.HOST = os.environ.get("JARBAS_HOST")
        self.mongo = db if db else MongoCore()

    def find_names(self, name):

        url = '%s?search=%s' % (self.HOST, quote(name))

        response = requests.get(url)

        b = []
        for x in response.json()['results']:
            if (name in x['congressperson_name']):
                b.append([x['congressperson_name'], x['applicant_id']])

        b.sort()
        names = list(b for b, _ in itertools.groupby(b))
        for x in names:
            logging.info('Adicionando politico: %s - %s', x[0], x[1])
            self.mongo.add_congressperson_to_list(x[0], x[1])
        return names

    def find_suspicions(self, id):

        url = '%s?suspicions=1&applicant_id=%s' % (self.HOST, id)

        response = requests.get(url)
        b = [x for x in response.json()['results']]

        return b
