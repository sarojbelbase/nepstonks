import re
from datetime import date
from os import path, remove
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup as bs
from nepali_datetime import date as nepdate

import utils.store as store
from utils.const import CATEGORIES, current_dir
from utils.models import Stock, session


def replace_this(substring: str, from_given_text: str) -> str:
    return re.sub(substring, '', from_given_text).strip()


def extract_units(sharetype: str) -> Optional[str]:
    index = sharetype.find(':')
    if index != -1:
        # get only kittas/units and slice out the "share_type"
        return sharetype[index+1:].strip()
    return None


def mark_as_published(given_item) -> None:
    given_item.is_published = True
    return session.add(given_item)


def parse_miti(given_date: date) -> str:
    miti = nepdate.from_datetime_date(given_date)
    return miti.strftime('%B %d')


def parse_date(given_date: date) -> str:
    return given_date.strftime('%B %d')


def is_rightshare(stock: Stock) -> str:
    # if its right share it publishes both units & ratio else publish units only
    units = f"Total Units: {stock.units}"
    ratio = f"Ratio: {stock.ratio}"
    if stock.ratio:
        return f"{units}, {ratio}"
    else:
        return units


def media_url_resolves(media_url: str) -> bool:
    """Checks if the given media url resolves (if it has the media)

    Args:
        media_url (str): the full url of the media

    Returns:
        bool: returns False if it can't resolve the generated media link
         from the given media link else returns True
    """
    if media_url:
        request = requests.get(media_url)
        return True if request.status_code == 200 else False
    else:
        return False


def handle_response(the_url: str, payload: dict, **kwargs):
    # handles telegram bot requests and raise if it can't
    try:
        req = requests.post(
            url=the_url,
            data=payload,
            files=kwargs['files'] if kwargs else None
        )
        res = req.json()
        if req.status_code == 200:
            if kwargs:
                from actions.save import add_chat
                add_chat(kwargs['stock_id'], res['result']['message_id'])
            print(req.json())
            return True
        return print("Sorry the telegram API didn't treat us good:\n", res)
    except requests.exceptions.HTTPError as error:
        return print("Looks like the telegram API did an oopsie:\n", error.response.json())


def merge_sources(*sources: list) -> List[Dict]:
    new_list = []
    for item in sources:
        new_list += item
    return new_list


def break_this(given_text: str) -> str:
    text = given_text.split()
    for i in range(0, len(text), 3):
        if i != 0:
            text[i-1] = f"{text[i-1]}\n"
    return ' '.join(text)


def flush_the_image() -> bool:
    picture = current_dir / store.image_name
    if store.image_name and path.exists(picture):
        remove(picture)
        return True
    else:
        return False


def get_sharetype(stock_id: int, raw_info: str) -> Optional[str]:
    local = "[Ll]ocals?"
    if CATEGORIES.get(stock_id):
        if bool(re.search(local, raw_info)):
            return f'Local {CATEGORIES.get(stock_id)}'
        return CATEGORIES.get(stock_id)
    return None


def hashtag(given_str: str) -> str:
    # remove spaces between two words
    return f"#{''.join(given_str.split())}"


def html_scraper(url):

    parser = 'lxml'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return print("Looks like the stock API did an oopsie:\n", e)
    else:
        return bs(response.text, parser)
