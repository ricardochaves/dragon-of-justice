import asyncio
import logging
import os
import sys

import telepot
from corebot.corebot import CoreBot
from telepot.aio.loop import MessageLoop

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


async def on_chat_message(msg):
    content_type, _, chat_id = telepot.glance(msg)
    if content_type != "text":
        return

    corebot = CoreBot()
    msgs = corebot.execute_command(msg["text"], chat_id)

    for m in msgs:
        await bot.sendMessage(chat_id, m, parse_mode="html")


if __name__ == "__main__":
    bot = telepot.aio.Bot(os.environ["TELEGRAM_BOT_TOKEN"])
    answerer = telepot.aio.helper.Answerer(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, {"chat": on_chat_message}).run_forever())
    logging.info("Listening ....")
    loop.run_forever()
