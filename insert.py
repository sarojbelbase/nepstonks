from sqlalchemy.orm import Query

from models import Stock, session
from fetch import latest_stocks

StockTable = Query(Stock, session)


def add_stock():

    try:
        scraped_stocks: list = latest_stocks()
        fetched_stocks: int = len(scraped_stocks)
    except Exception:
        raise ConnectionError('Sorry, we couldn\'t connect to the API.')

    for the_stock in scraped_stocks:
        the_stock_id = StockTable.filter(
            Stock.investment_id == the_stock['investment_id']).first()

        # to avoid adding same stock in the database
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


def unsent_stocks():
    return StockTable.filter(Stock.is_published == False).order_by(Stock.start_date.desc()).all()


def mark_as_published(stock):
    stock.is_published = True
    session.add(stock)
