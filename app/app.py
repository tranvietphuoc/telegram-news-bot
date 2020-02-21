from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from models import Info


url = 'https://vnexpress.net'


# get the respone from vnexpress.net
def get_soup():
    try:
        response = requests.get(url)
    except HTTPError:
        print(f'something went wrong with your requests')
        exit(1)
    return response


# generate the list of all class Item name
def generate_list_item():
    list_item = []
    for index in range(1, 19):
        item_name = 'Item-' + str(i)
        list_item.append(item_name)

    return list_item


# get all tag_a of the topnews of vnexpress.net
def extract_data():
    result = {}
    soup = BeautifulSoup(get_soup().text, 'html.parser')
    tag_a = soup.find_all('a')
    for link in tag_a:
        if link['class'] in generate_list_item():
            result.update(link['href'], link.string])

    return result

