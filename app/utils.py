from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from app.models import Info
from app import session_scope
from sqlalchemy import extract
from datetime import datetime
import json
import schedule
import time


# get the respone from vnexpress.net
def get_soup(url):
    """Get data from url"""
    try:
        response = requests.get(url)
    except HTTPError:
        print(f'something went wrong with your requests')
        exit(1)
    return response


# generate the list of all class Item name
def generate_list_items():
    """Generate a list of names of data-medium attribute of vnexpress page"""
    items = []
    for index in range(1, 19):
        item_name = 'Item-' + str(index)
        items.append(item_name)

    return items


# a dictionary to save the data extracted from vnexpress page

# get all tag_a of the topnews of vnexpress.net
def extract_data(url, items):
    """Get data from url and extract theme follow Database schema"""
    data_extracted = {}

    soup = BeautifulSoup(get_soup(url).content, 'html.parser')
    tags_a = soup.body.find_all('a')  # get all a tags in body, return a list
    # loop through a's list, then check if the attribute
    # data-medium is existed in every a tag, then save into
    # the result dictionary
    for link in tags_a:
        try:
            if link.attrs['data-medium'] in items:
                data_extracted.update({link.attrs['href']: link.string})
        except KeyError:
            continue

    return json.dumps(data_extracted)


# save informations into table
def save_data(url, items):
    """Save data crawled to database"""
    data = json.loads(extract_data(url, items))
    # data = extract_data(url, items)
    with session_scope() as session:
        for link, content in data.items():
            info = Info(link=link, content=content)
            session.add(info)

        session.commit()


def schedule_crawl(func, url, items):
    """Auto crawl data every 6 hours"""
    schedule.every(6).hours.do(func, url, items)
    while True:
        schedule.run_pending()
        time.sleep(10)


def load_data(date_time):
    """Query data from database"""
    # extract function to extract day, month, year in date_added of database
    # a simple query data if the day of query is the same of Info.date_added
    # use context manager of session_scope()
    with session_scope() as session:
        return session.query(Info).filter(
            extract('day', Info.date_added) == date_time.day,
            extract('month', Info.date_added) == date_time.month,
            extract('year', Info.date_added) == date_time.year).all()


# clean old data from database if they're storaged over 2 day
# use a simple query to get data to delete
def clean_data():
    """Clean old data from database"""
    # use context manager of session_scope()
    with session_scope() as session:
        old_data = session.query(Info).filter(extract('day', Info.date_added) <
                                              datetime.today().day,
                                              extract('month', Info.date_added) <=
                                              datetime.today().month,
                                              extract('year', Info.date_added) <=
                                              datetime.today().year).all()
        for data in old_data:
            session.delete(data)

        session.commit()


def schedule_clean(func):
    """Auto clean data every 2 days"""
    schedule.every(2).days.do(func)
    while True:
        schedule.run_pending()
        time.sleep(10)
