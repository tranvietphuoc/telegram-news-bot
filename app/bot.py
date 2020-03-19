from telegram.ext import (Updater, CommandHandler,
                          InlineQueryHandler, Dispatcher, run_async)
from app.utils import load_data
from datetime import datetime
import logging


# you can place your token here
# use logging module to know when things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s\
                    - %(message)s',
                    level=logging.INFO)


@run_async
def start(update, context):
    chat_id = update.message.chat_id
    text = "Hi there, please type /news to get the news!"
    context.bot.send_message(chat_id=chat_id, text=text)


@run_async
def news(update, context):
    # load data from database
    info = load_data(datetime.utcnow())
    chat_id = update.message.chat_id

    if info is None:
        context.bot.send_message(chat_id=chat_id,
                                 text="Sorry! There is no content!")

    # print(info)
    # if content is None then pass
    for i in info:
        if i.content is None:
            continue
        else:
            message = (i.content + ' - ' + i.link)
            context.bot.send_message(chat_id=chat_id, text=message)


def main(token):
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('news', news))
    updater.start_polling()
    updater.idle()
