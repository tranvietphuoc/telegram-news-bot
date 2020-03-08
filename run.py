from app.bot import main
from app.utils import save_data, generate_list_items, clean_data
import sched
import time


if __name__ == '__main__':
    URL = 'https://vnexpress.net'

    # clean old data from database
    clean_data()

    scheduler = sched.scheduler(time.time, time.sleep)
    # auto crawl after each 60 seconds
    scheduler.enter(60, 1, save_data,
                    argument=(URL, generate_list_items(),),
                    kwargs={})
    scheduler.run()
    main()
