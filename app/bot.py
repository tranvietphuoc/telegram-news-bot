from telegram.ext import (Updater, CommandHandler,
                          InlineQueryHandler, Dispatcher)
from telegram.ext import run_async
from app.utils import (generate_list_items, save_data,
                       datetime_to_int, load_data)
from app import session
from datetime import datetime


URL = 'https://vnexpress.net'

MY_TOKEN = '984695585:AAHE0knIkpzxo6SkeK55bgemJLz4L_elTHk'


@run_async
def news(update, context):
    info = load_data(datetime_to_int(datetime.utcnow()))
    chat_id = update.effective_chat.id
    for i in info:
        message = i.content + i.link
        context.bot.send_message(chat_id=chat_id, message=message)


def main():
    updater = Updater(MY_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('news', news))
    updater.start_polling()
    updater.idle()


