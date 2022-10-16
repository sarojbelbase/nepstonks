from actions import (add_announcements, add_stocks, publish_announcement,
                     publish_stock, remind_and_pin, unsent_announcements,
                     unsent_stocks, upcoming_stocks)
from utils.models import session


def publish_stocks():

    # Fetch and store new stocks before
    # publishing to the telegram channel
    add_stocks()

    unpublished_stocks = unsent_stocks()

    if not unpublished_stocks:
        return

    for the_stock in unpublished_stocks:
        publish_stock(the_stock)

    session.commit()
    return print(f"Published {len(unpublished_stocks)} Stocks")


def publish_announcements():

    # Fetch and store new announcements before
    # publishing to the telegram channel
    add_announcements()

    unpublished_announcements = unsent_announcements()

    if not unpublished_announcements:
        return

    for announcement in unpublished_announcements:
        publish_announcement(announcement)

    session.commit()
    return print(f"Published {len(unpublished_announcements)} Announcements")


def remind_stock():
    upcoming_issues = list(upcoming_stocks())
    if upcoming_issues:
        for issue in upcoming_issues:
            remind_and_pin(issue)
        return print(f"Reminded about {len(upcoming_issues)} Stocks")


if __name__ == '__main__':
    publish_stocks()
    publish_announcements()
    remind_stock()
