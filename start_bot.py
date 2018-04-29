import sys
import telepot
import asyncio
import logging

from telepot.aio.loop import MessageLoop

from db import insert
from db import addOne
from db import removeOne
from db import getOne
from db import get_politico_name
from requests_jarbas import find_names
from requests_jarbas import find_suspecius


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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


async def send_all_suspicions(chat_id, data):

    logging.info('send_all_suspicions data: %s', data)

    await bot.sendMessage(chat_id, data['texto'])

    for i in data['message_itens']:
        await bot.sendMessage(chat_id, i['texto'], parse_mode='html')


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


async def on_chat_message(msg):
    logging.info('processando %s', msg)

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != 'text':
        return

    ind_pass = False

    texto_list = msg['text'].split(' ')
    command = texto_list[0]
    texto_list.pop(0)

    resposta = 'Não entendi, digite /ajuda para saber mais.'
    if command == '/nome':
        nome = ' '.join(texto_list)
        if nome:
            list_name = '\n\n'.join(['<strong>%s</strong>.\n -- Para seguir use /seguir_%s\n -- Para fiscalizar use /passado_%s' %
                                     (x[0], x[1], x[1]) for x in find_names(nome)])
            resposta = "A pesquisa pelo nome <strong>%s</strong> gerou os seguintes resultados: \n %s" % (
                nome, list_name)
        else:
            resposta = "Você não usou o comando /nome corretamente, depois de digitar /nome você deve digitar na frente do comando o nome do político que você quer seguir."

    elif command == '/ajuda':
        resposta = 'Commandos disponíveis:\n\n/nome fulano\n/lista\n\nUtilizando esses dois comandos você já será capaz de utilizar o bot. Esses comando vão mostras as outras opções que você tem'

    elif command == '/lista':
        lista = '\n\n'.join(['<strong>%s</strong>.\n -- Para ver o históricos: /passado_%s\n -- Para parar de seguir /cancelar_%s' %
                             (get_politico_name(x["id"]), x["id"], x["id"]) for x in getOne(chat_id)])
        resposta = 'Você está seguindo os seguintes políticos: \n%s' % lista
    elif command == '/start':
        insert(chat_id)
        resposta = 'Bem vindo ao Controle Público, aqui você pode verificar as atividades suspeitas dos seus candidatos, para saber como funciona a detecção de uma informação suspeita você pode ler mais em www.serenata.ai. \nAgora me diga qual o deputado você quer seguir. Funciona da seguinte forma, digite o seguinte: \n \n/nome fulano \n \nTodos os deputádos que tem fulano no nome ou sobrenome irão aparecer na lista. \nPara saber mais sobre o bot digite /ajuda.'

    else:
        texto_list = msg['text'].split('_')
        if texto_list[0] == '/cancelar':
            removeOne(chat_id, texto_list[1])
            resposta = 'Você deixou de seguir %s.' % get_politico_name(texto_list[1])
        elif texto_list[0] == '/seguir':
            addOne(chat_id, texto_list[1])
            resposta = 'Agora você está seguindo %s. Para parar de seguir use /cancelar_%s.\n\nPara ver a lista de todos os deputados seguidos user /lista' % (
                get_politico_name(texto_list[1]), texto_list[1])
        elif texto_list[0] == '/passado':
            resposta = build_msg_suspicions(find_suspecius(texto_list[1]))
            await send_all_suspicions(chat_id, resposta)
            ind_pass = True

    if not ind_pass:
        await bot.sendMessage(chat_id, resposta, parse_mode='html')


async def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(
        msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    await bot.answerCallbackQuery(query_id, text='Got it')


TOKEN = '565523066:AAFPPRapI5AhtaME26NSJMCp1bEuHB2UvaE'
bot = telepot.aio.Bot(TOKEN)

answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
                                   'callback_query': on_callback_query}).run_forever())
logging.info('Listening ....')
loop.run_forever()
