from .const import BOT_TOKEN, CHANNEL
import requests

the_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def handle_response(method, the_url, payload):
    try:
        if method == 'get':
            response = requests.get(the_url)
        else:
            response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)


def send_message(message):
    message_url = the_url + 'sendMessage'
    payload = {
        'chat_id': CHANNEL,
        'text': message,
        'parse_mode': 'HTML'
    }
    return handle_response('post', message_url, payload)


def send_photo(image_url, caption):
    photo_url = the_url + 'sendPhoto'
    payload = {
        'chat_id': CHANNEL,
        'photo': image_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    return handle_response('post', photo_url, payload)


def set_webhook(base_url):
    webhook_url = the_url + 'setWebhook'
    payload = {
        'url': base_url + BOT_TOKEN
    }
    return handle_response('post', webhook_url, payload)


def get_webhook_info():
    info_url = the_url + 'getWebhookInfo'
    return handle_response('get', info_url, None)


def delete_webhook():
    remove_url = the_url + 'deleteWebhook'
    return handle_response('get', remove_url, None)
