import os
import requests
import itertools
import logging

from urllib.parse import quote
from urllib.parse import parse_qs

from corebot.db import MongoCore


class Requester:

    def __init__(self, db=None):

        self.HOST = os.environ.get("JARBAS_HOST")
        self.mongo = db if db else MongoCore()

    def find_names(self, name):

        url = '%s?search=%s' % (self.HOST, quote(name))

        response = requests.get(url)

        b = [[x['congressperson_name'], x['applicant_id']] for x in response.json()['results'] if
             name.upper() in x['congressperson_name']]

        b.sort()
        names = list(b for b, _ in itertools.groupby(b))
        for x in names:
            logging.info('Adicionando politico: %s - %s', x[0], x[1])
            self.mongo.add_congressperson_to_list(x[0], x[1])
        return names

    def find_suspicions(self, applicant_id, offset=""):

        url = '%s?suspicions=1&applicant_id=%s&limit=7&offset=%s' % (self.HOST, applicant_id, offset)
        print(url)
        response = requests.get(url)
        suspicions_list = [x for x in response.json()['results']]
        next_offset = parse_qs(response.json()["next"]).get("offset", [""])[0]

        return suspicions_list, next_offset
