from app.bot import main
from app.utils import save_data, generate_list_items, clean_data
from multiprocessing import Process


if __name__ == '__main__':
    URL = 'https://vnexpress.net'
    items = generate_list_items()

    # clean old data from database
    clean_data()
    p1 = Process(target=save_data, args=(URL, items,))
    p1.start()
    p2 = Process(target=main)
    p2.start()
    p1.join()
    p2.join()
    
    # scheduler = sched.scheduler(time.time, time.sleep)
    # auto crawl after each 60 seconds
    # scheduler.enter(60, 1, save_data,
    #                argument=(URL, items),
    #                kwargs={})
    # scheduler.run()
    # main()
