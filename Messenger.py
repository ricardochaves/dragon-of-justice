import logging
import sys

class Messenger:

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def __init__(self):
        pass

    def create_item_message(data):
        logging.info('create_item_message data: %s', data)

        item = {
            "texto": "<strong>Ano:</strong> %s\n"
                     "<strong>Quota:</strong> %s\n"
                     "<strong>Grupo Quota:</strong> %s\n"
                     "<strong>Fornecedor:</strong> %s\n"
                     "<strong>CNPJ Fornecedo:</strong> %s\n"
                     "<strong>Data:</strong> %s\n"
                     "<strong>Documento Id:</strong> %s\n"
                     "<strong>Valor:</strong> %s\n"
                     "<strong>MOTIVO:</strong> %s\n"
                     "<a href='%s'>MAIS INFORMAÇÕES DO JARBAS CLIQUE AQUI:</a>\n"
                     "<strong>Link Nota Fiscal:</strong> %s\n" % (
                         data['year'],
                         data['subquota_description'],
                         data['subquota_group_description'],
                         data['supplier'],
                         data['cnpj_cpf'],
                         data['issue_date'],
                         data['document_id'],
                         data['document_value'],
                         build_suspicions(data['suspicions']),
                         'https://jarbas.serenata.ai/layers/#/documentId/%s' % data['document_id'],
                         data['receipt']['url'] if data['receipt']['url'] else 'Não cadastrado'
                     )
        }

        return item

    def build_msg_suspicions(lista):
        logging.info('build_msg_suspicions lista: %s', lista)
        itens = [create_item_message(x) for x in lista]

        if len(lista) > 0:
            core_texto = 'Abaixo dessa mensagem você vai receber uma mensagem para cada ocorrencia do %s' % lista[
                0]["congressperson_name"]
        else:
            core_texto = 'Não foi encontrada nenhuma ocorrencia para o político'
        core_message = {
            "texto": core_texto,
            "message_itens": itens
        }
        return core_message

    def create_item_message(data):
        logging.info('create_item_message data: %s', data)

        item = {
            "texto": "<strong>Ano:</strong> %s\n"
                     "<strong>Quota:</strong> %s\n"
                     "<strong>Grupo Quota:</strong> %s\n"
                     "<strong>Fornecedor:</strong> %s\n"
                     "<strong>CNPJ Fornecedo:</strong> %s\n"
                     "<strong>Data:</strong> %s\n"
                     "<strong>Documento Id:</strong> %s\n"
                     "<strong>Valor:</strong> %s\n"
                     "<strong>MOTIVO:</strong> %s\n"
                     "<a href='%s'>MAIS INFORMAÇÕES DO JARBAS CLIQUE AQUI:</a>\n"
                     "<strong>Link Nota Fiscal:</strong> %s\n" % (
                         data['year'],
                         data['subquota_description'],
                         data['subquota_group_description'],
                         data['supplier'],
                         data['cnpj_cpf'],
                         data['issue_date'],
                         data['document_id'],
                         data['document_value'],
                         build_suspicions(data['suspicions']),
                         'https://jarbas.serenata.ai/layers/#/documentId/%s' % data['document_id'],
                         data['receipt']['url'] if data['receipt']['url'] else 'Não cadastrado'
                     )
        }

        return item

    def build_suspicions(data):
        if 'irregular_companies_classifier' in data.keys():
            return 'Companhia (Fornecedor) irregular. Situação cadastral inválida ou não tem permissão para vender o tipo de produto ou serviço.'

        elif 'election_expenses_classifier' in data.keys():
            return data

        elif 'meal_price_outlier_classifier' in data.keys():
            return 'Valor suspeito de refeição'

        elif 'monthly_subquota_limit_classifier' in data.keys():
            return 'Limite da Quota mensal atingido'

        elif 'traveled_speeds_classifier' in data.keys():
            return 'Viagens muito rápidas'

        return data