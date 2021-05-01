from insert import add_stock, unsent_stocks, upcoming_stocks
from telegram import publish_stock, remind_and_pin


def publish_stocks():
    # fetch and store new stocks before publishing to the channel
    add_stock()

    unpublished_stocks = list(unsent_stocks())
    if len(unpublished_stocks) > 0:
        from models import session
        for the_stock in unpublished_stocks:
            publish_stock(the_stock)
        session.commit()
        return print(f"published {len(unpublished_stocks)} stocks")


def remind_stock():
    upcoming_issues = list(upcoming_stocks())
    if len(upcoming_issues) > 0:
        for issue in upcoming_issues:
            remind_and_pin(issue)
        return print(f"reminded about {len(upcoming_issues)} stock")


if __name__ == '__main__':
    publish_stocks()
    remind_stock()
