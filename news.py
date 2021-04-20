from unicodedata import normalize

import requests
from bs4 import BeautifulSoup as bs


def scrape_articles(url: str):
    parser = 'lxml'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
    except Exception as error:
        print("Cannot connect to the server.", error)
    content = response.text.encode('utf-8')
    soup = bs(content, parser)
    return soup


def bleach(given_text: str) -> str:
    extra_space = normalize('NFKD', given_text)
    return extra_space.replace('\n', '')
