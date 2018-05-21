import os
import requests
import requests_mock
from urllib.parse import quote

from corebot.db import MongoCore


def cleardb():
    mongo = MongoCore()
    mongo.user_list_collection.remove({})
    mongo.congressperson_collection.remove({})


def mock_json_jarbas_search():
    return {
        "count": 1758046,
        "next": "https://jarbas.serenata.ai/api/chamber_of_deputies/reimbursement/?limit=7&offset=7&type=json",
        "previous": "null",
        "results": [
                {
                    "all_net_values": [
                        6000.0
                    ],
                    "all_reimbursement_numbers": [
                        6118
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 6000.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/3059/2018/6490316.pdf"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 6000.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6490316,
                    "last_update": "2018-04-30T16:47:59.577999-03:00",
                    "year": 2018,
                    "applicant_id": 3059,
                    "congressperson_id": 137070,
                    "congressperson_name": "VICENTINHO JÚNIOR",
                    "congressperson_document": 66,
                    "party": "PR",
                    "state": "TO",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 120,
                    "subquota_description": "Automotive vehicle renting or charter",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "VIP SERVICE CLUB LOCADORA E SERVICOS LTDA",
                    "cnpj_cpf": "02605452000122",
                    "document_type": 1,
                    "document_number": "1709",
                    "issue_date": "2018-02-01",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1460406,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'02605452000122':10A 'automotiv':13 'chart':17 'club':5A 'júnior':2A 'locador':6A 'ltda':9A 'or':16 'pr':11A 'renting':15 'servic':4A,8A 'to':12B 'vehicl':14 'vicentinh':1A 'vip':3A"
                },
            {
                    "all_net_values": [
                        14900.0
                    ],
                    "all_reimbursement_numbers": [
                        6115
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 14900.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/1651/2018/6490091.pdf"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 14900.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6490091,
                    "last_update": "2018-04-30T16:47:56.781564-03:00",
                    "year": 2018,
                    "applicant_id": 1651,
                    "congressperson_id": 74383,
                    "congressperson_name": "GIACOBO",
                    "congressperson_document": 466,
                    "party": "PR",
                    "state": "PR",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 119,
                    "subquota_description": "Aircraft renting or charter of aircraft",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "HELISUL TAXI AEREO LTDA",
                    "cnpj_cpf": "75543611000185",
                    "document_type": 0,
                    "document_number": "000218",
                    "issue_date": "2018-02-01",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1460298,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'75543611000185':6A 'aer':4A 'aircraft':9,14 'chart':12 'giacob':1A 'helisul':2A 'ltda':5A 'of':13 'or':11 'pr':7A,8B 'renting':10 'tax':3A"
                    },
            {
                    "all_net_values": [
                        6990.0
                    ],
                    "all_reimbursement_numbers": [
                        6114
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 6990.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/3048/2018/6488461.pdf"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 6990.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6488461,
                    "last_update": "2018-04-30T16:47:59.568892-03:00",
                    "year": 2018,
                    "applicant_id": 3048,
                    "congressperson_id": 178840,
                    "congressperson_name": "ROCHA",
                    "congressperson_document": 59,
                    "party": "PSDB",
                    "state": "AC",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 5,
                    "subquota_description": "Publicity of parliamentary activity",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "MOBOBITS LTDA - ME",
                    "cnpj_cpf": "21138576000190",
                    "document_type": 0,
                    "document_number": "0064",
                    "issue_date": "2018-01-31",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1459790,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'21138576000190':4A 'ac':6B 'activity':10 'ltda':3A 'mobobits':2A 'of':8 'parliamentary':9 'psdb':5A 'publicity':7 'roch':1A"
                    },
            {
                    "all_net_values": [
                        5780.0
                    ],
                    "all_reimbursement_numbers": [
                        6117
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 5780.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "null"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 5780.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6489767,
                    "last_update": "2018-04-30T16:47:57.027027-03:00",
                    "year": 2018,
                    "applicant_id": 2916,
                    "congressperson_id": 178907,
                    "congressperson_name": "FRANCISCO CHAPADINHA",
                    "congressperson_document": 28,
                    "party": "PODE",
                    "state": "PA",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 3,
                    "subquota_description": "Fuels and lubricants",
                    "subquota_group_id": 1,
                    "subquota_group_description": "Veículos Automotores",
                    "supplier": "PETROSAN COMERCIO DE COMBUSTIVEIS LTDA",
                    "cnpj_cpf": "14082069000116",
                    "document_type": 4,
                    "document_number": "12161",
                    "issue_date": "2018-01-31",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1460177,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'14082069000116':8A 'and':12 'automotor':15 'chapadinh':2A 'combustiv':6A 'comerci':4A 'francisc':1A 'fuels':11 'ltda':7A 'lubricants':13 'pa':10B 'petrosan':3A 'pod':9A 'veícul':14"
                    },
            {
                    "all_net_values": [
                        3000.0
                    ],
                    "all_reimbursement_numbers": [
                        6114
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 3000.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "null"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 3000.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6488892,
                    "last_update": "2018-04-30T16:47:56.927700-03:00",
                    "year": 2018,
                    "applicant_id": 2354,
                    "congressperson_id": 160515,
                    "congressperson_name": "RONALDO BENEDET",
                    "congressperson_document": 484,
                    "party": "PMDB",
                    "state": "SC",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 120,
                    "subquota_description": "Automotive vehicle renting or charter",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "E C BARRETO TURISMO EIRELI - ME",
                    "cnpj_cpf": "03514281000199",
                    "document_type": 4,
                    "document_number": "128",
                    "issue_date": "2018-01-31",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1459897,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'03514281000199':8A 'automotiv':11 'barret':5A 'benedet':2A 'c':4A 'chart':15 'eirel':7A 'or':14 'pmdb':9A 'renting':13 'ronald':1A 'sc':10B 'turism':6A 'vehicl':12"
                    },
            {
                    "all_net_values": [
                        130.0
                    ],
                    "all_reimbursement_numbers": [
                        6117
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 130.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "null"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 130.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6488779,
                    "last_update": "2018-04-30T16:47:56.906095-03:00",
                    "year": 2018,
                    "applicant_id": 2282,
                    "congressperson_id": 160653,
                    "congressperson_name": "ROBERTO DE LUCENA",
                    "congressperson_document": 385,
                    "party": "PV",
                    "state": "SP",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 14,
                    "subquota_description": "Lodging, except for congressperson from Distrito Federal",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "HOTEL NACIONAL S/A",
                    "cnpj_cpf": "72629140000134",
                    "document_type": 4,
                    "document_number": "124911",
                    "issue_date": "2018-01-31",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1459870,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'72629140000134':7A 'congressperson':13 'distrit':15 'except':11 'federal':16 'from':14 'hotel':4A 'lodging':10 'lucen':3A 'nacional':5A 'pv':8A 'robert':1A 's/a':6A 'sp':9B"
                    },
            {
                    "all_net_values": [
                        200.0
                    ],
                    "all_reimbursement_numbers": [
                        6114
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 200.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "null"
                    },
                    "rosies_tweet": "null",
                    "remark_value": 0.0,
                    "total_net_value": 200.0,
                    "total_reimbursement_value": 0.0,
                    "document_id": 6489268,
                    "last_update": "2018-04-30T16:47:56.804952-03:00",
                    "year": 2018,
                    "applicant_id": 1798,
                    "congressperson_id": 141405,
                    "congressperson_name": "CELSO MALDANER",
                    "congressperson_document": 472,
                    "party": "PMDB",
                    "state": "SC",
                    "term_id": 55,
                    "term": 2015,
                    "subquota_id": 5,
                    "subquota_description": "Publicity of parliamentary activity",
                    "subquota_group_id": 0,
                    "subquota_group_description": "",
                    "supplier": "Empresa Jornalística Jornal Expressão Ltda - ME",
                    "cnpj_cpf": "08657922000188",
                    "document_type": 4,
                    "document_number": "1861",
                    "issue_date": "2018-01-31",
                    "month": 1,
                    "installment": 0,
                    "batch_number": 1460036,
                    "passenger": "",
                    "leg_of_the_trip": "",
                    "suspicions": "null",
                    "receipt_text": "null",
                    "search_vector": "'08657922000188':8A 'activity':14 'cels':1A 'empres':3A 'expressã':6A 'jornal':5A 'jornalíst':4A 'ltda':7A 'maldan':2A 'of':12 'parliamentary':13 'pmdb':9A 'publicity':11 'sc':10B"
                    }
        ]
    }


def mock_json_jarbas_suspicions():
    return {
        "count": 8584,
        "next": "https://jarbas.serenata.ai/api/chamber_of_deputies/reimbursement/?limit=7&offset=7&suspicions=1",
        "previous": "null",
        "results": [
                {
                    "all_net_values": [
                        70.52
                    ],
                    "all_reimbursement_numbers": [
                        6093
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 70.52,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'17314329004460':8A 'alimentaca':6A 'andrad':2A 'company':5A 'congressperson':11 'international':3A 'meal':4A,12 'mg':10B 'pp':9A 'renat':1A 's.a':7A"
                },
            {
                    "all_net_values": [
                        57.25
                    ],
                    "all_reimbursement_numbers": [
                        6082
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 57.25,
                    "probability": "null",
                    "receipt": {
                        "fetched": True,
                        "url": "http://www.camara.gov.br/cota-parlamentar/documentos/publ/527/2017/6475653.pdf"
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
                    "suspicions": {
                        "invalid_cnpj_cpf": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'aprendizag':6A 'colatt':2A 'comercial':7A 'congressperson':11 'meal':12 'nacional':4A 'pmdb':9A 'sc':10B 'senac':8A 'servic':3A 'vald':1A"
                },
            {
                    "all_net_values": [
                        671.85
                    ],
                    "all_reimbursement_numbers": [
                        6051
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 671.85,
                    "probability": "null",
                    "receipt": {
                        "fetched": False,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'03953506000103':9A 'belin':4A 'congressperson':10 'gastronom':7A 'lideranc':1A 'ltda':8A 'meal':11 'paes':5A 'psdb':3A"
                },
            {
                    "all_net_values": [
                        600.0
                    ],
                    "all_reimbursement_numbers": [
                        6054
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 600.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": False,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'33447301000117':7A 'aliment':5A 'comerci':3A 'congressperson':8 'ltda':6A 'meal':9 'phs':1A 'taiob':2A"
                },
            {
                    "all_net_values": [
                        1600.0
                    ],
                    "all_reimbursement_numbers": [
                        6080
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 1600.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": False,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'26171763000199':10A 'buffet':5A 'congressperson':11 'gourmet':7A 'lim':4A 'ltda':9A 'ltda-m':8A 'maison':6A 'meal':12 'sdd':1A 'vasconcel':2A"
                },
            {
                    "all_net_values": [
                        538.72
                    ],
                    "all_reimbursement_numbers": [
                        6080
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 538.72,
                    "probability": "null",
                    "receipt": {
                        "fetched": False,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'03346671000954':8A 'cd':2A 'congressperson':9 'epp':7A 'lid.gov':1A 'ltda':6A 'meal':10 'self':4A 'servic':5A 'taiob':3A"
                },
            {
                    "all_net_values": [
                        2880.0
                    ],
                    "all_reimbursement_numbers": [
                        6046
                    ],
                    "all_reimbursement_values": [
                        0.0
                    ],
                    "document_value": 2880.0,
                    "probability": "null",
                    "receipt": {
                        "fetched": False,
                        "url": "null"
                    },
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
                    "suspicions": {
                        "meal_price_outlier": True
                    },
                    "receipt_text": "null",
                    "search_vector": "'18440959168':7A '27570249000199':8A 'antoni':4A 'borg':6A 'congressperson':9 'girott':5A 'lideranc':1A 'meal':10 'pt':3A"
                }
        ]
    }


def mock_request_search():
    url = '%s?search=%s' % (os.environ.get("JARBAS_HOST"), quote('fulano'))
    session = requests.Session()
    adapter = requests_mock.Adapter()
    adapter.register_uri('GET', url, json=mock_json_jarbas_search())
    session.mount('mock', adapter)
