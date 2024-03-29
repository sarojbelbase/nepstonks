from datetime import date
from typing import List

from sqlalchemy.orm import Query

from actions.scrape import scrape_announcements, scrape_stocks
from utils import Announcement, Stock, Telegram, enums, session, store

# Query objects from the database
StockTable = Query(Stock, session)
TelegramTable = Query(Telegram, session)
AnnouncementTable = Query(Announcement, session)


def add_stocks() -> None:

    # First of all, scrape new stocks
    print("Scraping stocks from the API")
    scrape_stocks()
    print(f"Scraped {len(store.new_stocks)} stocks")
    added_stocks = 0

    # Check if there are any new stocks else return None
    if not store.new_stocks:
        return

    for stock in store.new_stocks:

        # Only ordinary shares are added to the database
        if stock.get('share_type') != enums.ShareType.ordinary.value:
            continue

        # Check if they are already in the database
        the_stock = StockTable\
            .filter(Stock.id == stock['id'])\
            .first()

        # Check if the stock is already in the database
        if not the_stock:
            this_stock = Stock(**stock)
            session.add(this_stock)
            added_stocks += 1

    session.commit()
    print(f"Added {added_stocks} stocks to the database")


def add_announcements() -> None:

    # First of all, scrape new announcements
    print("Scraping Announcements...")
    scrape_announcements()

    # Check if there are any new announcements else return None
    if not store.new_announcements:
        return

    # Add new announcements to the database
    for announcement in store.new_announcements:

        the_announcement = AnnouncementTable\
            .filter(Announcement.content_url == announcement['content_url'])\
            .first()

        # Check if the announcement is already in the database
        if not the_announcement:
            this_announcement = Announcement(**announcement)
            session.add(this_announcement)

    session.commit()

    print(f"Added {len(store.new_announcements)} Announcements")


def add_chat(stock_id: int, message_id: int) -> bool:
    the_stock = StockTable.filter(Stock.id == stock_id).first()
    if the_stock and message_id:
        chat = \
            Telegram(
                stock=the_stock,
                message_id=message_id
            )
        session.add(chat)
        session.commit()
        return True
    return False


def unsent_stocks() -> List[Stock]:
    # only send stocks that are newer
    return StockTable.filter(Stock.is_published == False, Stock.opening_date >= date.today()).order_by(Stock.opening_date.desc()).all()


def upcoming_stocks() -> List[Stock]:
    # lists all issues that are about to open today
    return StockTable.filter(Stock.opening_date == date.today()).order_by(Stock.opening_date.desc()).all()


def unsent_announcements() -> List[Announcement]:
    # only send stocks that are newer or not published
    return AnnouncementTable.filter(Announcement.is_published == False).order_by(Announcement.scraped_at.desc()).all()
