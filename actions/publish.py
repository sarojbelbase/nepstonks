from typing import Optional

from typing_extensions import Literal

from utils import (CHANNEL, TELEGRAM_URL, Announcement, Stock, flush_the_image,
                   handle_response, humanize_number, mark_as_published)


def send_this_stock(stock: Stock) -> Optional[Literal[True]]:
    from actions.generate_image import generate
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


def send_this_announcement(announcement: Announcement) -> Optional[Literal[True]]:
    endpoint = TELEGRAM_URL + 'sendMessage'
    payload = {
        'text': announcement_content(announcement),
        'disable_web_page_preview': True,
        'parse_mode': 'HTML',
        'chat_id': CHANNEL
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
    from utils.helpers import hashtag
    first_line = f"<strong>#Stock #IPO #{stock.stock_symbol}</strong>"
    second_line = f"<strong>{hashtag(stock.sector_name)}</strong>"
    return f'{first_line} · {second_line}'


def announcement_content(announcement: Announcement) -> str:
    return f"""<strong>📢 Share Allotment Announcement!</strong>

{announcement.content}

<strong><a href="{announcement.content_url}">View Announcement</a></strong>
"""


def reminding_content(stock: Stock) -> str:
    return f"""<strong>Reminder!</strong>

<strong>Don't forget to apply for this IPO today.😊</strong>
<strong>{stock.company_name}</strong>
<strong>{f"Total Units: {humanize_number(stock.units)}"}</strong>
"""


def publish_stock(the_stock: Stock) -> bool:
    if send_this_stock(the_stock):
        mark_as_published(the_stock)
        flush_the_image()
        return True
    return False


def publish_announcement(the_announcement: Announcement) -> bool:
    if send_this_announcement(the_announcement):
        mark_as_published(the_announcement)
        return True
    return False


def remind_and_pin(the_stock: Stock) -> bool:
    if the_stock.chat.message_id:
        send_reminder(the_stock)
        pin_message(the_stock)
        return True
    return False
