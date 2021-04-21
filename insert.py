from sqlalchemy.orm import Query

from fetch import latest_stocks
from models import News, Stock, session
from news import bizmandu

StockTable = Query(Stock, session)
NewsTable = Query(News, session)


def add_stock():

    try:
        scraped_stocks: list = latest_stocks()
        fetched_stocks: int = len(scraped_stocks)
    except Exception as error:
        print("Sorry couldn't connect to the API.", error)

    for the_stock in scraped_stocks:
        the_stock_id = StockTable.filter(
            Stock.investment_id == the_stock['investment_id']).first()

        # to avoid inserting the same stock in the table
        if not the_stock_id and fetched_stocks > 0:
            this_stock = \
                Stock(
                    company_name=the_stock['company_name'],
                    end_date=the_stock['end_date'],
                    investment_id=the_stock['investment_id'],
                    issued_by=the_stock['issued_by'],
                    pdf=the_stock['pdf'],
                    ratio=the_stock['ratio'],
                    start_date=the_stock['start_date'],
                    stock_id=the_stock['stock_id'],
                    stock_symbol=the_stock['stock_symbol'],
                    stock_type=the_stock['stock_type'],
                    units=the_stock['units']
                )
            session.add(this_stock)
    session.commit()


def add_article():

    try:
        scraped_articles: list = bizmandu()
        fetched_articles: int = len(scraped_articles)
    except Exception as error:
        print("Sorry couldn't connect to the API.", error)

    for the_article in scraped_articles:
        the_article_id = NewsTable.filter(
            News.title == the_article['title']).first()

        # to avoid inserting the same article in the table
        if not the_article_id and fetched_articles > 0:
            this_article = \
                News(
                    date_published=the_article['date_published'],
                    description=the_article['description'],
                    image_url=the_article['image_url'],
                    lang=the_article['lang'],
                    source=the_article['source'],
                    title=the_article['title'],
                    url=the_article['url'],
                )
            session.add(this_article)
    session.commit()


def unsent_stocks():
    return StockTable.filter(Stock.is_published == False).order_by(Stock.start_date.desc()).all()


def unsent_articles():
    return NewsTable.filter(News.is_published == False).order_by(News.date_published.desc()).all()
