from insert import add_stock, unsent_stocks, upcoming_stocks
from telegram import remind_and_pin


def add_and_publish_stocks():
    # fetch and store new stocks before publishing to the channel
    add_stock()

    unpublished_stocks = list(unsent_stocks())
    if len(unpublished_stocks) > 0:
        from image import generate
        from models import session
        generate(unpublished_stocks)
        session.commit()
        return print(f"published {len(unpublished_stocks)} stocks")


def remind_about_the_stock():
    upcoming_issues = list(upcoming_stocks())
    if len(upcoming_issues) > 0:
        for issue in upcoming_issues:
            remind_and_pin(issue)
        return print(f"reminded about {len(upcoming_issues)} stock")


if __name__ == '__main__':
    add_and_publish_stocks()
    # remind_about_the_stock()
