import requests
import itertools
import logging

from urllib.parse import quote

from db import add_politico

class Requester:

    def __init__(self):
        # TODO - Move to config file
        self.HOST = 'https://jarbas.serenata.ai/api/'

    def find_names(self, name):

        end_point = 'chamber_of_deputies/reimbursement/?search=%s' % quote(name)

        response = requests.get('%s%s' % (self.HOST, end_point))

        b = [[x['congressperson_name'], x['applicant_id']] for x in response.json()['results']]
        b.sort()
        names = list(b for b, _ in itertools.groupby(b))
        for x in names:
            logging.info('Adicionando politico: %s - %s', x[0], x[1])
            add_politico(x[0], x[1])
        return names


    def find_suspecius(self, id):

        end_point = 'chamber_of_deputies/reimbursement/?suspicions=1&applicant_id=%s' % id

        response = requests.get('%s%s' % (self.HOST, end_point))
        b = [x for x in response.json()['results']]

        return b
