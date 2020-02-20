from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from models import Info


url = 'https://vnexpress.net'


# get the respone from vnexpress.net
def getSoup():
    try:
        respone = requests.get(url)
    except HTTPError:
        print(f'something went wrong with your requests')
        exit(1)
    return respone


soup = BeautifulSoup(getSoup().text, 'html.parser')

