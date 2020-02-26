from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from models import Info


URL = 'https://vnexpress.net'


# get the respone from vnexpress.net
def get_soup():
    try:
        response = requests.get(URL)
    except HTTPError:
        print(f'something went wrong with your requests')
        exit(1)
    return response


# generate the list of all class Item name
def generate_list_item():
    list_item = []
    for index in range(1, 19):
        item_name = 'Item-' + str(index)
        list_item.append(item_name)

    return list_item


# get all tag_a of the topnews of vnexpress.net
def extract_data():
    result = {}
    list_item = generate_list_item()
    soup = BeautifulSoup(get_soup().content, 'html.parser')
    tags_a = soup.body.find_all('a')  # get all a tags in body, return a list
    # loop through a's list, then check if the attribute
    # data-medium is existed in every a tag, then save into
    # the result dictionary
    for link in tags_a:
        try:
            if link.attrs['data-medium'] in list_item:
                result.update({link.attrs['href']: link.string})
        except KeyError:
            continue
    
    return result

# save informations into table
def save_data():
    info = Info()

# print(extract_data())
