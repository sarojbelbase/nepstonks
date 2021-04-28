from sqlalchemy.orm import Query

from fetch import latest_stocks
from models import News, Stock, Telegram, session
from news import latest_articles

NewsTable = Query(News, session)
StockTable = Query(Stock, session)
TelegramTable = Query(Telegram, session)


def add_stock():
    scraped_stocks: list = latest_stocks()
    fetched_stocks: int = len(scraped_stocks)
    if fetched_stocks > 0:
        for the_stock in scraped_stocks:
            the_stock_id = StockTable.filter(
                Stock.investment_id == the_stock['investment_id']).first()
            # to avoid inserting the same stock in the table
            if not the_stock_id:
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
    scraped_articles: list = latest_articles()
    fetched_articles: int = len(scraped_articles)
    if fetched_articles > 0:
        for the_article in scraped_articles:
            the_article_id = NewsTable.filter(
                News.title == the_article['title']).first()
            # to avoid inserting the same article in the table
            if not the_article_id:
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


def add_chat(stock_id: int, message_id: int):
    the_stock = StockTable.filter(Stock.id == stock_id).first()
    if the_stock and message_id:
        chat = \
            Telegram(
                stock=the_stock,
                message_id=message_id
            )
        session.add(chat)
        session.commit()


def unsent_stocks():
    return StockTable.filter(Stock.is_published == False).order_by(Stock.start_date.desc()).all()


def upcoming_stocks():
    from datetime import date, timedelta
    # lists all stock that are one day far from being available to apply
    one_day_far = date.today() + timedelta(days=1)
    return StockTable.filter(Stock.start_date == one_day_far).order_by(Stock.start_date.desc()).all()


def unsent_articles():
    return NewsTable.filter(News.is_published == False).order_by(News.date_published.desc()).all()
