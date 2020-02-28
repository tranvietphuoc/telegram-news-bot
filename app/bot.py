from telegram.ext import (Updater, CommandHandler,
                          InlineQueryHandler, Dispatcher)
from telegram.ext import run_async
from app.utils import (get_soup, generate_list_item,
                       extract_data, save_data, load_data)
from app import session
from datetime import datetime


URL = 'https://vnexpress.net'

MY_TOKEN = '984695585:AAHE0knIkpzxo6SkeK55bgemJLz4L_elTHk'


@run_async
def news(update, context):
    info = load_data(datetime.utcnow)
    chat_id = update.message.chat_id
    for i in info:
        message = i.content + i.link
        context.bot.send_message(chat_id=chat_id, message=message)


def main():
    updater = Updater(MY_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('news', news))
    updater.start_polling()
    updater.idle()


