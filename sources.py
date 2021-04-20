import re

from dateutil import parser as ps

from const import NEWS_URL_BM
from news import bleach, fix_last_dharko, scrape_articles

# this file contains all the news sources that we can scrape news from


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
            "title": bleach(title),
            "source": source,
            "description": fix_last_dharko(bleach(description)),
            "url": url,
            "image_url": None,
            "timestamp": date,
            "lang": "nepali",
        }

        articles.append(the_article)

    return articles
