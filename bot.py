import requests

from const import CHANNEL, TELEGRAM_URL


def handle_response(the_url, payload):
    try:
        response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)


def publish_stock(content):
    message_url = TELEGRAM_URL + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': content,
        'parse_mode': 'HTML'
    }
    return handle_response(message_url, payload)
