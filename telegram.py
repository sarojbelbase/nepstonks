from datetime import date

import requests
from nepali_datetime import date as nepdate

from const import CHANNEL, HORI_LINE, TELEGRAM_URL


def handle_response(the_url, payload):
    try:
        response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)


def publish_stock(stock_detail: str):
    message_url = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': parsed_content(stock_detail),
        'disable_web_page_preview': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(message_url, payload)


def parsed_content(stock: str) -> str:
    return f"""
<strong><i>New {stock.stock_type} Alert!</i></strong>
{HORI_LINE}
<strong>{stock.company_name}</strong>
Issued by: <strong>{stock.issued_by}</strong>
Start Date: <strong>{parse_miti(stock.start_date)} / {parse_date(stock.start_date)}</strong>
End Date: <strong>{parse_miti(stock.end_date)} / {parse_date(stock.end_date)}</strong>
Stock Type: <strong>{stock.stock_type}</strong>
{is_rightshare(stock)}
Stock Symbol: <strong>{stock.stock_symbol}</strong>
Investment ID: <strong>{stock.investment_id}</strong>
Description: <strong><a href="https://sidbelbase.me/">See PDF</a></strong>
{HORI_LINE}
    """


def parse_miti(given_date: date) -> str:
    miti = nepdate.from_datetime_date(given_date)
    return miti.strftime('%B %d')


def parse_date(given_date: date) -> str:
    return given_date.strftime('%B %d')


def is_rightshare(stock: str) -> str:
    # if its right share, publish both units and ratios else units only
    units = f"Units: <strong>{stock.units}</strong>"
    ratio = f"Ratio: <strong>{stock.ratio}</strong>"
    if stock.ratio:
        return f"{units}\n{ratio}"
    else:
        return units


def get_pdf_link(pdf_name: str) -> str:
    pass


# :TODO:
# Find PDF URL
