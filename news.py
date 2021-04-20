import re
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


def fix_last_dharko(given_text: str) -> str:
    dharko = '।'
    matches = re.finditer(dharko, given_text)
    all_dharkos = [match.start() for match in matches]
    index_of_last_dharko = max(all_dharkos)
    # also include the dharko after slicing the given text
    fixed_text = given_text[:index_of_last_dharko+1]
    return fixed_text
