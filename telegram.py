from typing import Optional

from typing_extensions import Literal

from const import CHANNEL, TELEGRAM_URL
from models import Stock
from utils import (flush_the_image, handle_response, is_rightshare,
                   mark_as_published)


def send_this_stock(stock: Stock) -> Optional[Literal[True]]:
    from image import generate
    endpoint = TELEGRAM_URL + 'sendPhoto'
    payload = {
        'chat_id': CHANNEL,
        'caption': stock_content(stock),
        'parse_mode': 'HTML'
    }
    files = {'photo': generate(stock)}
    return handle_response(endpoint, payload, files=files, record_response=True, stock_id=stock.id)


def send_reminder(stock: Stock) -> Optional[Literal[True]]:
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': reminding_content(stock),
        'reply_to_message_id': stock.chat.message_id,
        'parse_mode': 'HTML'
    }
    return handle_response(endpoint, payload)


def pin_message(stock: Stock) -> Optional[Literal[True]]:
    endpoint = TELEGRAM_URL + 'pinChatMessage'
    payload = {
        'chat_id': CHANNEL,
        'message_id': stock.chat.message_id,
    }
    return handle_response(endpoint, payload)


def stock_content(stock: Stock) -> str:
    from utils import hashtag
    without_pdf = f"<strong>#Stock {hashtag(stock.stock_type)} #{stock.scrip}</strong>"
    with_pdf = f'<strong><a href="{stock.pdf_url}">View PDF</a></strong>'
    return f'{without_pdf} · {with_pdf}' if stock.pdf_url else without_pdf


def reminding_content(stock: Stock) -> str:
    return f"""<strong>Reminder!</strong>

<strong>Don't forget to apply for this {stock.stock_type} today.😊</strong>
<strong>{stock.company_name}</strong>
<strong>{is_rightshare(stock)}</strong>
"""


def publish_stock(the_stock: Stock) -> bool:
    if send_this_stock(the_stock):
        mark_as_published(the_stock)
        flush_the_image(the_stock)
        return True
    return False


def remind_and_pin(the_stock: Stock) -> bool:
    if the_stock.chat.message_id:
        send_reminder(the_stock)
        pin_message(the_stock)
        return True
    return False
