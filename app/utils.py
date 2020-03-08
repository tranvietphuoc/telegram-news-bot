from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from app.models import session, Info
from sqlalchemy import extract
from datetime import datetime


# get the respone from vnexpress.net
def get_soup(url):
    try:
        response = requests.get(url)
    except HTTPError:
        print(f'something went wrong with your requests')
        exit(1)
    return response


# generate the list of all class Item name
def generate_list_items():
    items = []
    for index in range(1, 19):
        item_name = 'Item-' + str(index)
        items.append(item_name)

    return items


# get all tag_a of the topnews of vnexpress.net
def extract_data(url, items):
    result = {}
    soup = BeautifulSoup(get_soup(url).content, 'html.parser')
    tags_a = soup.body.find_all('a')  # get all a tags in body, return a list
    # loop through a's list, then check if the attribute
    # data-medium is existed in every a tag, then save into
    # the result dictionary
    for link in tags_a:
        try:
            if link.attrs['data-medium'] in items:
                result.update({link.attrs['href']: link.string})
        except KeyError:
            continue
 
    return result


# save informations into table
def save_data(url, items):
    data = extract_data(url, items)
    for link, content in data.items():
        info = Info(link=link, content=content)
        session.add(info)

    session.commit()


def load_data(date_time):
    # extract function to extract day, month, year in date_added of database
    # query data if the day of query is the same of Info.date_added
    # and the substraction of the hour of query and Info.date_added
    # greater than 1
    return session.query(Info).filter(
        extract('day', Info.date_added) == date_time.day,
        extract('month', Info.date_added) == date_time.month,
        extract('year', Info.date_added) == date_time.year,
        date_time.hour - extract('hour', Info.date_added) >= 1).all()


# clean old data from database
def clean_data():
    old_data = session.query(Info).filter(extract('day', Info.date_added) <
                                          datetime.today().day,
                                          extract('month', Info.date_added) <=
                                          datetime.today().month,
                                          extract('year', Info.date_added) <=
                                          datetime.today().year).all()
    for data in old_data:
        session.delete(data)
    session.commit()
