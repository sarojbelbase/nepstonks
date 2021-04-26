from const import CHANNEL, PDF_URL, TELEGRAM_URL
from utils import (handle_response, has_description, is_rightshare,
                   mark_as_published, parse_date, parse_miti, media_url_resolves)


def send_only_content(stock: str):
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': parsed_stock_content(stock),
        'disable_web_page_preview': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload, True, stock.id)


def send_with_pdf(stock: str):
    endpoint = TELEGRAM_URL + 'sendDocument'
    pdf = PDF_URL + stock.pdf
    payload = {
        'chat_id': CHANNEL,
        'document': pdf,
        'caption': parsed_stock_content(stock),
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload, True, stock.id)


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


def send_with_photo(article: str):
    endpoint = TELEGRAM_URL + 'sendPhoto'
    payload = {
        'chat_id': CHANNEL,
        'photo': article.image_url,
        'caption': parsed_article_content(article),
        'disable_web_page_preview': 'true',
        'disable_notification': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def send_reminder(stock: str):
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': reminding_content(stock),
        'reply_to_message_id': stock.chat.message_id,
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def pin_message(stock: str):
    endpoint = TELEGRAM_URL + 'pinChatMessage'
    payload = {
        'chat_id': CHANNEL,
        'message_id': stock.chat.message_id,
    }
    return handle_response(endpoint, payload)


def parsed_article_content(article: str) -> str:
    return f"""
<strong>{article.title}</strong>

{has_description(article)}
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


def reminding_content(stock: str) -> str:
    return f"""
<strong>Reminder!</strong>

Don't forget to apply for this {stock.stock_type} tomorrow😊.
<strong>{stock.company_name} | {stock.stock_symbol}</strong>
{is_rightshare(stock)}
"""


def publish_stock(the_stock):
    from const import PDF_URL
    pdf_url = PDF_URL + the_stock.pdf
    if media_url_resolves(pdf_url):
        send_with_pdf(the_stock)
        mark_as_published(the_stock)
    else:
        send_only_content(the_stock)
        mark_as_published(the_stock)


def remind_and_pin(the_stock) -> bool:
    if the_stock.chat.message_id:
        send_reminder(the_stock)
        pin_message(the_stock)
        return True


def publish_article(the_article):
    image_url = the_article.image_url
    if media_url_resolves(image_url):
        send_with_photo(the_article)
        mark_as_published(the_article)
    else:
        send_only_article(the_article)
        mark_as_published(the_article)
