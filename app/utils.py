from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from app.models import session, Info


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
    return session.query(Info).filter((Info.date_added <= date_time) and
                                  (datetime_to_int(Info.date_added) == 
                                  datetime_to_int(date_time)))


def datetime_to_int(date_time):
    return int(date_time.strftime('%Y%m%d'))


