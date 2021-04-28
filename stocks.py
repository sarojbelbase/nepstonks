from insert import add_stock, unsent_stocks, upcoming_stocks
from telegram import publish_stock, remind_and_pin


def add_and_publish_stocks():
    # fetch and store new stocks before publishing to the channel
    add_stock()

    unpublished_stocks = list(unsent_stocks())
    if len(unpublished_stocks) > 0:
        # stocks that are older has to be published first
        # making the latest ones to be after the older ones
        the_list = unpublished_stocks[::-1]
        for the_stock in the_list:
            publish_stock(the_stock)
        from models import session
        session.commit()
        return {"ok": "true"}


def remind_about_the_stock():
    upcoming_issues = list(upcoming_stocks())
    if len(upcoming_issues) > 0:
        for issue in upcoming_issues:
            remind_and_pin(issue)
        return {"ok": "true"}


if __name__ == '__main__':
    add_and_publish_stocks()
    remind_about_the_stock()
