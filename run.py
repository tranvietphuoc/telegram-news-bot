from app.bot import main
from app.utils import save_data, generate_list_items, clean_data
import sched
import time


if __name__ == '__main__':
    URL = 'https://vnexpress.net'
    scheduler = sched.scheduler(time.time, time.sleep)
    # auto crawl after each 6 hours
    scheduler.enter(6*3600, 1, save_data, (URL, generate_list_items(),))
    scheduler.run()
    main()
