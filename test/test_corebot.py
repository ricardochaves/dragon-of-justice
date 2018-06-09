
import os
import sys
import unittest
from test.helper import cleardb
from test.helper import mock_json_jarbas_search
from test.helper import mock_json_jarbas_suspicions
from urllib.parse import quote

import requests_mock
from corebot.corebot import CoreBot
from corebot.db import MongoCore
from corebot.simple_messenger import SimpleHtmlMessenger

sys.path.append("..")


class TestCoreBot(unittest.TestCase):
    def setUp(self):
        cleardb()
        self.message = SimpleHtmlMessenger()

    def test_command_start(self):
        """
            Test: Integration: CoreBot: Command /start
        """
        corebot = CoreBot()
        msg = corebot.execute_command("/start", 123)
        self.assertEqual(msg, self.message.start_message())

    def test_command_help(self):
        """
            Test: Integration: CoreBot: Command /start
        """
        corebot = CoreBot()
        msg = corebot.execute_command("/ajuda", 123)
        self.assertEqual(msg, self.message.help_message())

    def test_command_list(self):
        """
            Test: Integration: CoreBot: Command /lista
        """
        mongo = MongoCore()
        mongo.insert_user(123)
        mongo.add_congressperson_to_list("fulano", 444)
        mongo.add_congressperson_to_list("fulano2", 555)
        mongo.add_congressperson_to_follow(123, 444)
        mongo.add_congressperson_to_follow(123, 555)

        corebot = CoreBot()
        msg = corebot.execute_command("/lista", 123)

        self.assertEqual(msg, self.message.user_user_following([["fulano", 444], ["fulano2", 555]]))

    def test_command_follow(self):
        """
            Test: Integration: CoreBot: Command /seguir_XXX
        """
        mongo = MongoCore()
        mongo.insert_user(123)
        mongo.add_congressperson_to_list("fulano", 444)
        mongo.add_congressperson_to_list("fulano2", 555)

        corebot = CoreBot()

        msg = corebot.execute_command("/seguir_444", 123)

        self.assertEqual(msg, self.message.follow_congressperson("fulano", 444))

    def test_command_unfollow(self):
        """
            Test: Integration: CoreBot: Command /deixardeseguir_XXX
        """
        mongo = MongoCore()
        mongo.insert_user(123)
        mongo.add_congressperson_to_list("fulano", 444)
        mongo.add_congressperson_to_list("fulano2", 555)
        mongo.add_congressperson_to_follow(123, 444)
        mongo.add_congressperson_to_follow(123, 555)

        corebot = CoreBot()

        msg = corebot.execute_command("/deixardeseguir_444", 123)

        self.assertEqual(msg, self.message.unfollow_congressperson("fulano"))

    @requests_mock.mock()
    def test_command_name(self, r):
        """
            Test: Integration: CoreBot: Command /name
        """

        url = "%s?search=%s" % (os.environ.get("JARBAS_HOST"), quote("vicentinho"))

        expected_name = [["VICENTINHO JÚNIOR", 3059]]

        r.get(url, json=mock_json_jarbas_search())

        corebot = CoreBot()
        corebot.execute_command("/start", 123)
        msg = corebot.execute_command("/nome vicentinho", 123)

        self.assertEqual(msg, self.message.names_list("vicentinho", expected_name))

    @requests_mock.mock()
    def test_command_history(self, r):
        """
            Test: Integration: CoreBot: Command /historico
        """
        mongo = MongoCore()
        mongo.insert_user(123)
        mongo.add_congressperson_to_list("fulano", 444)

        url = "%s?suspicions=1&applicant_id=%s" % (os.environ.get("JARBAS_HOST"), 444)
        expected_suspicions = [
            {
                "all_net_values": [70.52],
                "all_reimbursement_numbers": [6093],
                "all_reimbursement_values": [0.0],
                "document_value": 70.52,
                "probability": "null",
                "receipt": {"fetched": True, "url": "null"},
                "rosies_tweet": "https://twitter.com/RosieDaSerenata/status/971052962142355459",
                "remark_value": 0.0,
                "total_net_value": 70.52,
                "total_reimbursement_value": 0.0,
                "document_id": 6480727,
                "last_update": "2018-05-01T01:23:54.519861-03:00",
                "year": 2017,
                "applicant_id": 2817,
                "congressperson_id": 171620,
                "congressperson_name": "RENATO ANDRADE",
                "congressperson_document": 590,
                "party": "PP",
                "state": "MG",
                "term_id": 55,
                "term": 2015,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "INTERNATIONAL MEAL COMPANY ALIMENTACAO S.A.",
                "cnpj_cpf": "17314329004460",
                "document_type": 4,
                "document_number": "20967",
                "issue_date": "2017-12-27",
                "month": 12,
                "installment": 0,
                "batch_number": 1457077,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'17314329004460':8A 'alimentaca':6A 'andrad':2A 'company':5A 'congressperson':11 'international':3A 'meal':4A,12 'mg':10B 'pp':9A 'renat':1A 's.a':7A",
            },
            {
                "all_net_values": [57.25],
                "all_reimbursement_numbers": [6082],
                "all_reimbursement_values": [0.0],
                "document_value": 57.25,
                "probability": "null",
                "receipt": {
                    "fetched": True,
                    "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/527/2017/6475653.pdf",
                },
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 57.25,
                "total_reimbursement_value": 0.0,
                "document_id": 6475653,
                "last_update": "2018-05-01T01:28:49.147090-03:00",
                "year": 2017,
                "applicant_id": 527,
                "congressperson_id": 74010,
                "congressperson_name": "VALDIR COLATTO",
                "congressperson_document": 489,
                "party": "PMDB",
                "state": "SC",
                "term_id": 55,
                "term": 2015,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "SERVICO NACIONAL DE APRENDIZAGEM COMERCIAL SENAC",
                "cnpj_cpf": "",
                "document_type": 0,
                "document_number": "9757",
                "issue_date": "2017-12-26",
                "month": 12,
                "installment": 0,
                "batch_number": 1455335,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"invalid_cnpj_cpf": True},
                "receipt_text": "null",
                "search_vector": "'aprendizag':6A 'colatt':2A 'comercial':7A 'congressperson':11 'meal':12 'nacional':4A 'pmdb':9A 'sc':10B 'senac':8A 'servic':3A 'vald':1A",
            },
            {
                "all_net_values": [671.85],
                "all_reimbursement_numbers": [6051],
                "all_reimbursement_values": [0.0],
                "document_value": 671.85,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 671.85,
                "total_reimbursement_value": 0.0,
                "document_id": 6470297,
                "last_update": "2018-04-30T16:45:48.407950-03:00",
                "year": 2017,
                "applicant_id": 2442,
                "congressperson_id": "null",
                "congressperson_name": "LIDERANÇA DO PSDB",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "BELINI PAES E GASTRONOMIA LTDA",
                "cnpj_cpf": "03953506000103",
                "document_type": 0,
                "document_number": "930",
                "issue_date": "2017-12-19",
                "month": 12,
                "installment": 0,
                "batch_number": 1453005,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'03953506000103':9A 'belin':4A 'congressperson':10 'gastronom':7A 'lideranc':1A 'ltda':8A 'meal':11 'paes':5A 'psdb':3A",
            },
            {
                "all_net_values": [600.0],
                "all_reimbursement_numbers": [6054],
                "all_reimbursement_values": [0.0],
                "document_value": 600.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 600.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6469641,
                "last_update": "2018-04-30T16:47:30.790899-03:00",
                "year": 2017,
                "applicant_id": 3122,
                "congressperson_id": "null",
                "congressperson_name": "PHS",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "TAIOBA COMERCIO DE ALIMENTOS LTDA - ME",
                "cnpj_cpf": "33447301000117",
                "document_type": 4,
                "document_number": "3186",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1453516,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'33447301000117':7A 'aliment':5A 'comerci':3A 'congressperson':8 'ltda':6A 'meal':9 'phs':1A 'taiob':2A",
            },
            {
                "all_net_values": [1600.0],
                "all_reimbursement_numbers": [6080],
                "all_reimbursement_values": [0.0],
                "document_value": 1600.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 1600.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6473718,
                "last_update": "2018-04-30T16:45:52.908008-03:00",
                "year": 2017,
                "applicant_id": 2864,
                "congressperson_id": "null",
                "congressperson_name": "SDD",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "VASCONCELOS E LIMA BUFFET MAISON GOURMET LTDA-ME",
                "cnpj_cpf": "26171763000199",
                "document_type": 4,
                "document_number": "21",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1454591,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'26171763000199':10A 'buffet':5A 'congressperson':11 'gourmet':7A 'lim':4A 'ltda':9A 'ltda-m':8A 'maison':6A 'meal':12 'sdd':1A 'vasconcel':2A",
            },
            {
                "all_net_values": [538.72],
                "all_reimbursement_numbers": [6080],
                "all_reimbursement_values": [0.0],
                "document_value": 538.72,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 538.72,
                "total_reimbursement_value": 0.0,
                "document_id": 6471978,
                "last_update": "2018-04-30T16:45:52.144698-03:00",
                "year": 2017,
                "applicant_id": 2812,
                "congressperson_id": "null",
                "congressperson_name": "LID.GOV-CD",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "TAIOBA SELF SERVICE LTDA - EPP",
                "cnpj_cpf": "03346671000954",
                "document_type": 4,
                "document_number": "423",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1453733,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'03346671000954':8A 'cd':2A 'congressperson':9 'epp':7A 'lid.gov':1A 'ltda':6A 'meal':10 'self':4A 'servic':5A 'taiob':3A",
            },
            {
                "all_net_values": [2880.0],
                "all_reimbursement_numbers": [6046],
                "all_reimbursement_values": [0.0],
                "document_value": 2880.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 2880.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6466087,
                "last_update": "2018-04-30T16:45:48.361005-03:00",
                "year": 2017,
                "applicant_id": 2439,
                "congressperson_id": "null",
                "congressperson_name": "LIDERANÇA DO PT",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "ANTONIO GIROTTO BORGES 18440959168",
                "cnpj_cpf": "27570249000199",
                "document_type": 0,
                "document_number": "000792806",
                "issue_date": "2017-12-13",
                "month": 12,
                "installment": 0,
                "batch_number": 1451971,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'18440959168':7A '27570249000199':8A 'antoni':4A 'borg':6A 'congressperson':9 'girott':5A 'lideranc':1A 'meal':10 'pt':3A",
            },
        ]
        r.get(url, json=mock_json_jarbas_suspicions())

        corebot = CoreBot()
        msg = corebot.execute_command("/historico_444", 123)

        self.assertEqual(msg, self.message.history_message(expected_suspicions, 444, 7))

    @requests_mock.mock()
    def test_command_next(self, r):
        """
            Test: Integration: CoreBot: Command /proximos
        """
        mongo = MongoCore()
        mongo.insert_user(123)
        mongo.add_congressperson_to_list("fulano", 444)

        url = "%s?suspicions=1&applicant_id=%s" % (os.environ.get("JARBAS_HOST"), 444)
        expected_suspicions = [
            {
                "all_net_values": [70.52],
                "all_reimbursement_numbers": [6093],
                "all_reimbursement_values": [0.0],
                "document_value": 70.52,
                "probability": "null",
                "receipt": {"fetched": True, "url": "null"},
                "rosies_tweet": "https://twitter.com/RosieDaSerenata/status/971052962142355459",
                "remark_value": 0.0,
                "total_net_value": 70.52,
                "total_reimbursement_value": 0.0,
                "document_id": 6480727,
                "last_update": "2018-05-01T01:23:54.519861-03:00",
                "year": 2017,
                "applicant_id": 2817,
                "congressperson_id": 171620,
                "congressperson_name": "RENATO ANDRADE",
                "congressperson_document": 590,
                "party": "PP",
                "state": "MG",
                "term_id": 55,
                "term": 2015,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "INTERNATIONAL MEAL COMPANY ALIMENTACAO S.A.",
                "cnpj_cpf": "17314329004460",
                "document_type": 4,
                "document_number": "20967",
                "issue_date": "2017-12-27",
                "month": 12,
                "installment": 0,
                "batch_number": 1457077,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'17314329004460':8A 'alimentaca':6A 'andrad':2A 'company':5A 'congressperson':11 'international':3A 'meal':4A,12 'mg':10B 'pp':9A 'renat':1A 's.a':7A",
            },
            {
                "all_net_values": [57.25],
                "all_reimbursement_numbers": [6082],
                "all_reimbursement_values": [0.0],
                "document_value": 57.25,
                "probability": "null",
                "receipt": {
                    "fetched": True,
                    "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/527/2017/6475653.pdf",
                },
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 57.25,
                "total_reimbursement_value": 0.0,
                "document_id": 6475653,
                "last_update": "2018-05-01T01:28:49.147090-03:00",
                "year": 2017,
                "applicant_id": 527,
                "congressperson_id": 74010,
                "congressperson_name": "VALDIR COLATTO",
                "congressperson_document": 489,
                "party": "PMDB",
                "state": "SC",
                "term_id": 55,
                "term": 2015,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "SERVICO NACIONAL DE APRENDIZAGEM COMERCIAL SENAC",
                "cnpj_cpf": "",
                "document_type": 0,
                "document_number": "9757",
                "issue_date": "2017-12-26",
                "month": 12,
                "installment": 0,
                "batch_number": 1455335,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"invalid_cnpj_cpf": True},
                "receipt_text": "null",
                "search_vector": "'aprendizag':6A 'colatt':2A 'comercial':7A 'congressperson':11 'meal':12 'nacional':4A 'pmdb':9A 'sc':10B 'senac':8A 'servic':3A 'vald':1A",
            },
            {
                "all_net_values": [671.85],
                "all_reimbursement_numbers": [6051],
                "all_reimbursement_values": [0.0],
                "document_value": 671.85,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 671.85,
                "total_reimbursement_value": 0.0,
                "document_id": 6470297,
                "last_update": "2018-04-30T16:45:48.407950-03:00",
                "year": 2017,
                "applicant_id": 2442,
                "congressperson_id": "null",
                "congressperson_name": "LIDERANÇA DO PSDB",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "BELINI PAES E GASTRONOMIA LTDA",
                "cnpj_cpf": "03953506000103",
                "document_type": 0,
                "document_number": "930",
                "issue_date": "2017-12-19",
                "month": 12,
                "installment": 0,
                "batch_number": 1453005,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'03953506000103':9A 'belin':4A 'congressperson':10 'gastronom':7A 'lideranc':1A 'ltda':8A 'meal':11 'paes':5A 'psdb':3A",
            },
            {
                "all_net_values": [600.0],
                "all_reimbursement_numbers": [6054],
                "all_reimbursement_values": [0.0],
                "document_value": 600.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 600.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6469641,
                "last_update": "2018-04-30T16:47:30.790899-03:00",
                "year": 2017,
                "applicant_id": 3122,
                "congressperson_id": "null",
                "congressperson_name": "PHS",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "TAIOBA COMERCIO DE ALIMENTOS LTDA - ME",
                "cnpj_cpf": "33447301000117",
                "document_type": 4,
                "document_number": "3186",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1453516,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'33447301000117':7A 'aliment':5A 'comerci':3A 'congressperson':8 'ltda':6A 'meal':9 'phs':1A 'taiob':2A",
            },
            {
                "all_net_values": [1600.0],
                "all_reimbursement_numbers": [6080],
                "all_reimbursement_values": [0.0],
                "document_value": 1600.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 1600.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6473718,
                "last_update": "2018-04-30T16:45:52.908008-03:00",
                "year": 2017,
                "applicant_id": 2864,
                "congressperson_id": "null",
                "congressperson_name": "SDD",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "VASCONCELOS E LIMA BUFFET MAISON GOURMET LTDA-ME",
                "cnpj_cpf": "26171763000199",
                "document_type": 4,
                "document_number": "21",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1454591,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'26171763000199':10A 'buffet':5A 'congressperson':11 'gourmet':7A 'lim':4A 'ltda':9A 'ltda-m':8A 'maison':6A 'meal':12 'sdd':1A 'vasconcel':2A",
            },
            {
                "all_net_values": [538.72],
                "all_reimbursement_numbers": [6080],
                "all_reimbursement_values": [0.0],
                "document_value": 538.72,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 538.72,
                "total_reimbursement_value": 0.0,
                "document_id": 6471978,
                "last_update": "2018-04-30T16:45:52.144698-03:00",
                "year": 2017,
                "applicant_id": 2812,
                "congressperson_id": "null",
                "congressperson_name": "LID.GOV-CD",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "TAIOBA SELF SERVICE LTDA - EPP",
                "cnpj_cpf": "03346671000954",
                "document_type": 4,
                "document_number": "423",
                "issue_date": "2017-12-14",
                "month": 12,
                "installment": 0,
                "batch_number": 1453733,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'03346671000954':8A 'cd':2A 'congressperson':9 'epp':7A 'lid.gov':1A 'ltda':6A 'meal':10 'self':4A 'servic':5A 'taiob':3A",
            },
            {
                "all_net_values": [2880.0],
                "all_reimbursement_numbers": [6046],
                "all_reimbursement_values": [0.0],
                "document_value": 2880.0,
                "probability": "null",
                "receipt": {"fetched": False, "url": "null"},
                "rosies_tweet": "null",
                "remark_value": 0.0,
                "total_net_value": 2880.0,
                "total_reimbursement_value": 0.0,
                "document_id": 6466087,
                "last_update": "2018-04-30T16:45:48.361005-03:00",
                "year": 2017,
                "applicant_id": 2439,
                "congressperson_id": "null",
                "congressperson_name": "LIDERANÇA DO PT",
                "congressperson_document": "null",
                "party": "",
                "state": "",
                "term_id": "null",
                "term": 0,
                "subquota_id": 13,
                "subquota_description": "Congressperson meal",
                "subquota_group_id": 0,
                "subquota_group_description": "",
                "supplier": "ANTONIO GIROTTO BORGES 18440959168",
                "cnpj_cpf": "27570249000199",
                "document_type": 0,
                "document_number": "000792806",
                "issue_date": "2017-12-13",
                "month": 12,
                "installment": 0,
                "batch_number": 1451971,
                "passenger": "",
                "leg_of_the_trip": "",
                "suspicions": {"meal_price_outlier": True},
                "receipt_text": "null",
                "search_vector": "'18440959168':7A '27570249000199':8A 'antoni':4A 'borg':6A 'congressperson':9 'girott':5A 'lideranc':1A 'meal':10 'pt':3A",
            },
        ]
        r.get(url, json=mock_json_jarbas_suspicions())

        corebot = CoreBot()
        msg = corebot.execute_command("/proximos_444_2", 123)

        self.assertEqual(msg, self.message.history_message(expected_suspicions, 444, 7))
