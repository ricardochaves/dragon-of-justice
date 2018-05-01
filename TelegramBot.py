import os

import sys
import telepot
import logging

from db import insert
from db import addOne
from db import removeOne
from db import getOne
from db import get_politico_name

class TelegramBot:

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def __init__(self, telegram_bot_token, messenger, requester):

        # TODO - read token from environment variables

        self.__token = telegram_bot_token
        self.__bot = telepot.aio.Bot(self.__token)
        self.__answerer = telepot.aio.helper.Answerer(self.__bot)
        self.messenger = messenger
        self.requester = requester


    def get_bot(self):
        return self.__bot

    def get_answerer(self):
        return self.__answerer

    async def send_all_suspicions(self, chat_id, data):
        logging.info('send_all_suspicions data: %s', data)

        await self.__bot.sendMessage(chat_id, data['texto'])

        for i in data['message_itens']:
            await self.__bot.sendMessage(chat_id, i['texto'], parse_mode='html')

    async def on_chat_message(self, msg):
        logging.info('processando %s', msg)

        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        ind_pass = False

        texto_list = msg['text'].split(' ')
        command = texto_list[0]
        texto_list.pop(0)

        # TODO - move to TelegramBot class
        resposta = 'Não entendi, digite /ajuda para saber mais.'
        if command == '/nome':
            nome = ' '.join(texto_list)
            if nome:
                list_name = '\n\n'.join(
                    ['<strong>%s</strong>.\n -- Para seguir use /seguir_%s\n -- Para fiscalizar use /passado_%s' %
                     (x[0], x[1], x[1]) for x in self.requester.find_names(nome)])
                resposta = "A pesquisa pelo nome <strong>%s</strong> gerou os seguintes resultados: \n %s" % (
                    nome, list_name)
            else:
                resposta = "Você não usou o comando /nome corretamente, depois de digitar /nome você deve digitar na frente do comando o nome do político que você quer seguir."

        elif command == '/ajuda':
            resposta = 'Commandos disponíveis:\n\n/nome fulano\n/lista\n\nUtilizando esses dois comandos você já será capaz de utilizar o bot. Esses comando vão mostras as outras opções que você tem'

        elif command == '/lista':
            lista = '\n\n'.join(
                ['<strong>%s</strong>.\n -- Para ver o históricos: /passado_%s\n -- Para parar de seguir /cancelar_%s' %
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
                resposta = self.messenger.build_msg_suspicions(self.requester.find_suspecius(texto_list[1]))
                await self.send_all_suspicions(chat_id, resposta)
                ind_pass = True

        if not ind_pass:
            await self.__bot.sendMessage(chat_id, resposta, parse_mode='html')

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(
            msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)

        await self.__bot.answerCallbackQuery(query_id, text='Got it')
