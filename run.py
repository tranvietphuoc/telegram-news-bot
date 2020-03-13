from app.bot import main
from app.utils import (save_data, generate_list_items,
                       clean_data, schedule_crawl)
import concurrent.futures  # this module use for run this program parallely


if __name__ == '__main__':
    URL = 'https://vnexpress.net'
    items = generate_list_items()

    # use ThreadPoolExecutor-a pool of threads to excecute calls asynchronously
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        clean = executor.submit(clean_data)
        save = executor.submit(schedule_crawl, save_data, URL, items)
        runbot = executor.submit(main)

        clean.result()
        save.result()
        runbot.result()


