from app.bot import main
from app.utils import (save_data, generate_list_items,
                       clean_data, schedule_crawl, schedule_clean)
import concurrent.futures  # this module use for run this program parallely
import sys
import json


"""
This application use three threads to clean data,
handle telegram bot command to get and display data,
auto crawl data then save to database
"""
if __name__ == '__main__':
    URL = 'https://vnexpress.net'
    items = generate_list_items()

    # get the token of telegram bot
    if len(sys.argv) != 2:
        print(f'This program require the Telegram bot token!')
        exit(1)
    else:
        with open(sys.argv[1], 'r') as f:
            token = json.loads(f.read())['token']

    # use ThreadPoolExecutor-a pool of threads to excecute calls asynchronously
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        clean = executor.submit(schedule_clean, clean_data)
        save = executor.submit(schedule_crawl, save_data, URL, items)
        runbot = executor.submit(main, token)

        clean.result()
        save.result()
        runbot.result()


