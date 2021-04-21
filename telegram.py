from const import CHANNEL, PDF_URL, TELEGRAM_URL
from utils import (handle_response, is_rightshare, mark_as_published,
                   parse_date, parse_miti, pdf_url_resolves)


def send_only_content(stock_detail: str):
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': parsed_stock_content(stock_detail),
        'disable_web_page_preview': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def send_with_pdf(stock_detail: str):
    endpoint = TELEGRAM_URL + 'sendDocument'
    pdf = PDF_URL + stock_detail.pdf
    payload = {
        'chat_id': CHANNEL,
        'document': pdf,
        'caption': parsed_stock_content(stock_detail),
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def send_only_article(article: str):
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': parsed_article_content(article),
        'disable_web_page_preview': 'true',
        'disable_notification': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def parsed_article_content(article: str) -> str:
    return f"""
<strong>{article.title}</strong>\n
{article.description}\n
📣 <strong>{article.source.title()} · {parse_date(article.date_published)} · <a href="{article.url}">Read More</a></strong>
    """


def parsed_stock_content(stock: str) -> str:
    return f"""
📣 <strong>New Upcoming {stock.stock_type} Alert!</strong> 🆕\n
<strong>{stock.company_name}</strong>
Issued By: <strong>{stock.issued_by}</strong>
Start Date: <strong>{parse_miti(stock.start_date)} / {parse_date(stock.start_date)}</strong>
End Date: <strong>{parse_miti(stock.end_date)} / {parse_date(stock.end_date)}</strong>
Stock Type: <strong>{stock.stock_type}</strong>
{is_rightshare(stock)}
Stock Symbol: <strong>{stock.stock_symbol}</strong>
    """


def publish_stock(the_stock):
    if pdf_url_resolves(the_stock.pdf):
        send_with_pdf(the_stock)
        mark_as_published(the_stock)
    else:
        send_only_content(the_stock)
        mark_as_published(the_stock)


def publish_article(the_article):
    send_only_article(the_article)
    mark_as_published(the_article)
