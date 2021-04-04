from insert import add_stock, unsent_stocks
from telegram import publish_stock


def main():
    add_stock()
    unpublished_stocks = list(unsent_stocks())
    if len(unpublished_stocks) > 0:
        the_list = unpublished_stocks[::-1]
        for the_stock in the_list:
            publish_stock(the_stock)
        from models import session
        session.commit()
    return {"ok": "true"}


if __name__ == '__main__':
    main()
