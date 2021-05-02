from const import CHANNEL, PDF_URL, TELEGRAM_URL
from utils import (flush_the_image, handle_response, has_description,
                   is_rightshare, mark_as_published, media_url_resolves,
                   parse_date)


def send_this_stock(stock: str):
    from image import generate
    endpoint = TELEGRAM_URL + 'sendPhoto'
    payload = {
        'chat_id': CHANNEL,
        'caption': stock_content(stock),
        'parse_mode': 'HTML'
    }
    files = {'photo': generate(stock)}
    return handle_response(endpoint, payload, files=files, record_response=True, stock_id=stock.id)


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


def send_only_article(article: str):
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': article_content(article),
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
        'caption': article_content(article),
        'disable_web_page_preview': 'true',
        'disable_notification': 'true',
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def article_content(article: str) -> str:
    return f"""<strong>{article.title}</strong>

{has_description(article)}

📣 <strong>#News #{article.source.title()} · {parse_date(article.date_published)} · <a href="{article.url}">Read More</a></strong>
"""


def stock_content(stock: str) -> str:
    return f"""<strong>#Stock #{stock.stock_type} #{stock.stock_symbol}</strong>
<strong><a href="{PDF_URL+ stock.pdf }">View In Details | PDF</a></strong>
"""


def reminding_content(stock: str) -> str:
    return f"""<strong>Reminder!</strong>

Don't forget to apply for this {stock.stock_type} tomorrow😊.
<strong>{stock.company_name} | {stock.stock_symbol}</strong>
{is_rightshare(stock)}
"""


def publish_stock(the_stock):
    if send_this_stock(the_stock):
        mark_as_published(the_stock)
        flush_the_image(the_stock)
        return True
    return print("couldn't send the stock")


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
