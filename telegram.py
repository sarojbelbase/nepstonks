from datetime import date

import requests
from nepali_datetime import date as nepdate

from const import CHANNEL, HORI_LINE, PDF_URL, TELEGRAM_URL
from insert import mark_as_published


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
<strong>{article.title}</strong>
<strong>{parse_date(article.date_published)} | {article.source}</strong>
{article.description}
<a href="{article.url}"><strong>Read More</strong></a>
    """


def parsed_stock_content(stock: str) -> str:
    return f"""
<strong><i>New Upcoming {stock.stock_type} Alert!</i></strong>
{HORI_LINE}
<strong>{stock.company_name}</strong>
Issued by: <strong>{stock.issued_by}</strong>
Start Date: <strong>{parse_miti(stock.start_date)} / {parse_date(stock.start_date)}</strong>
End Date: <strong>{parse_miti(stock.end_date)} / {parse_date(stock.end_date)}</strong>
Stock Type: <strong>{stock.stock_type}</strong>
{is_rightshare(stock)}
Stock Symbol: <strong>{stock.stock_symbol}</strong>
Investment ID: <strong>{stock.investment_id}</strong>
{HORI_LINE}
    """


def parse_miti(given_date: date) -> str:
    miti = nepdate.from_datetime_date(given_date)
    return miti.strftime('%B %d')


def parse_date(given_date: date) -> str:
    return given_date.strftime('%B %d')


def is_rightshare(stock: str) -> str:
    # if its right share it publishes both units & ratio else publish units only
    units = f"Units: <strong>{stock.units}</strong>"
    ratio = f"Ratio: <strong>{stock.ratio}</strong>"
    if stock.ratio:
        return f"{units}\n{ratio}"
    else:
        return units


def pdf_url_resolves(pdf: str) -> bool:
    """Checks if the given pdf resolves (if it has pdf)

    Args:
        pdf (str): pdf filename with pdf extension

    Returns:
        bool: returns False if it can't resolve the generated pdf link
         from the given pdf else returns True
    """
    if pdf:
        pdf_url = PDF_URL + pdf
        request = requests.get(pdf_url)
        return True if request.status_code == 200 else False
    else:
        return False


def handle_response(the_url, payload):
    try:
        response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)


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
