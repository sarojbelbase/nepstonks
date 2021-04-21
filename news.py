import re
from unicodedata import normalize

import requests
from bs4 import BeautifulSoup as bs
from dateutil import parser as ps

from const import NEWS_URL_BM


# main section: goes to the given url and scrapes

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


# sources section: the article sources will be in this section organized by function names

def bizmandu():
    source = 'bizmandu'
    first_word = "काठमाडौं।"
    soup = scrape_articles(NEWS_URL_BM)
    container = soup.find("ul", attrs={'class': "uk-list"}).find_all("li")
    articles = []

    for article in container:
        # dont touch! just witness the magic
        url = article.find('a')['href']
        title = article.find('h3').text.strip()
        paragraph = article.find('p', text=re.compile(
            first_word), _class=False, id=False)
        desc_one = paragraph.get_text().split(first_word)[1].strip()
        desc_two = paragraph.findNext('p').text.strip()
        description = f'{desc_one} {desc_two}'
        raw_date = article.find(
            'p', {'class': 'uk-article-meta'}).text.strip()
        date = ps.parse(raw_date.split('बिजमाण्डू')[1].strip())

        the_article = {
            "date_published": date,
            "description": fix_last_dharko(bleach(description)),
            "image_url": None,
            "lang": "nepali",
            "source": source,
            "title": bleach(title),
            "url": url,
        }

        articles.append(the_article)

    return articles


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
