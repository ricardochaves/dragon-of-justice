import sys
import telepot
import asyncio
import logging

from telepot.aio.loop import MessageLoop

from Messenger import Messenger
from TelegramBot import TelegramBot
from requests_jarbas import Requester

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

messenger = Messenger()
telegram_bot = TelegramBot(
    messenger=messenger, telegram_bot_token=os.environ['TELEGRAM_BOT_TOKEN'], requester=Requester())
answerer = telegram_bot.get_answerer()

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(telegram_bot.get_bot(), {'chat': telegram_bot.on_chat_message,
                                                      'callback_query': telegram_bot.on_callback_query}).run_forever())
logging.info('Listening ....')
loop.run_forever()
