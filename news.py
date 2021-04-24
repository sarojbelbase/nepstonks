import re

import requests
from bs4 import BeautifulSoup as bs
from dateutil import parser as ps

from const import NEWS_URL_BM, NEWS_URL_ML
from telegram import publish_article
from utils import bleach, fix_last_dharko, merge_sources


# scrape section: a function that starts the scraping engine

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


def merolagani():
    source = 'merolagani'
    soup = scrape_articles(NEWS_URL_ML)
    container = soup.select('div.media-news')
    articles = []

    for article in container:
        # dont touch! just witness the magic
        raw_url = article.find('a')['href']
        url = f'https://{source}.com{raw_url}'
        title = article.select('h4.media-title > a')[0].text.strip()
        image_url = article.find('img')['src']
        raw_date = article.select('span.media-label')[0].text.strip()
        date = ps.parse(raw_date)

        the_article = {
            "date_published": date,
            "description": None,
            "image_url": image_url,
            "lang": "nepali",
            "source": source,
            "title": bleach(title),
            "url": url,
        }

        articles.append(the_article)

    return articles


# main section: combines all required functions and executes them

def latest_articles():
    return merge_sources(bizmandu(), merolagani())


def main():
    from insert import add_article, unsent_articles
    # fetch and store new articles before publishing to the channel
    add_article()

    unpublished_articles = list(unsent_articles())
    if len(unpublished_articles) > 0:
        # articles that are older has to be published first
        # making the latest ones to be after the older ones
        the_list = unpublished_articles[::-1]
        for the_article in the_list:
            publish_article(the_article)
        from models import session
        session.commit()
    return {"ok": "true"}


if __name__ == '__main__':
    main()
