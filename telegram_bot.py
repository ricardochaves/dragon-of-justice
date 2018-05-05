import os
import sys
import telepot
import asyncio
import logging

from telepot.aio.loop import MessageLoop

from corebot.corebot import CoreBot

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


async def on_chat_message(msg):
    content_type, _, chat_id = telepot.glance(msg)
    if content_type != 'text':
        return

    corebot = CoreBot()
    msgs = corebot.execute_command(msg['text'], chat_id)

    for m in msgs:
        await bot.sendMessage(chat_id, m, parse_mode='html')


async def on_callback_query(msg):
    return

bot = telepot.aio.Bot(os.environ['TELEGRAM_BOT_TOKEN'])
answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat': on_chat_message,
                                   'callback_query': on_callback_query}).run_forever())
logging.info('Listening ....')
loop.run_forever()
