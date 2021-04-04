from insert import add_stock, mark_as_published, unsent_stocks
from telegram import send_only_content, send_with_pdf


def main():
    # add_stock()
    unpublished_stocks = list(unsent_stocks())
    unpublished_counts: int = len(unpublished_stocks)
    if unpublished_counts > 0:
        the_list = unpublished_stocks[:unpublished_counts][::-1]
        for the_stock in the_list:
            if not the_stock.pdf:
                send_only_content(the_stock)
                mark_as_published(the_stock)
            else:
                send_with_pdf(the_stock)
                mark_as_published(the_stock)
        from models import session
        session.commit()
    return {"ok": "true"}


if __name__ == '__main__':
    main()
