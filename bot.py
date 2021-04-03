import requests

from const import BOT_TOKEN, CHANNEL

the_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def handle_response(the_url, payload):
    try:
        response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)


def publish_stock(content):
    message_url = the_url + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': content,
        'parse_mode': 'HTML'
    }
    return handle_response(message_url, payload)


def set_webhook(base_url):
    webhook_url = the_url + 'setWebhook'
    payload = {
        'url': base_url + BOT_TOKEN
    }
    return handle_response(webhook_url, payload)
