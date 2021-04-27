import re
from datetime import date
from typing import Dict, List
from unicodedata import normalize

import requests
from nepali_datetime import date as nepdate


def bleach(given_text: str) -> str:
    # replaces line breaks and extra spaces
    extra_space = normalize('NFKD', given_text)
    return extra_space.replace('\n', '')


def fix_last_dharko(given_text: str) -> str:
    # removes incomplete texts towards the end
    dharko = '।'
    matches = re.finditer(dharko, given_text)
    all_dharkos = [match.start() for match in matches]
    index_of_last_dharko = max(all_dharkos)
    # also include the dharko after slicing the given text
    fixed_text = given_text[:index_of_last_dharko+1]
    return fixed_text


def get_units(sharetype: str) -> str:
    index = sharetype.find(':')
    if index != -1:
        # get only kittas/units and slice out the "share_type"
        return sharetype[index+1:].strip()


def mark_as_published(given_item):
    from insert import session
    given_item.is_published = True
    session.add(given_item)


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


def has_description(article: str) -> str:
    # if the article has description return description else None
    return article.description if article.description else ''


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


def handle_response(the_url, payload, *args):
    # handles telegram bot requests and raise if it can't
    try:
        req = requests.post(the_url, data=payload)
        res = req.json()
        if True in args:
            if res['ok'] and req.status_code == 200:
                _, stock_id = args
                msg_id = res['result']['message_id']
                from insert import add_chat
                add_chat(stock_id, msg_id)
        return print(req.content)
    except requests.exceptions.HTTPError as error:
        return print("Looks like the telegram API did an oopsie:\n", error.response.json())


def merge_sources(*sources: list) -> List[Dict]:
    new_list = []
    for item in sources:
        new_list += item
    return new_list
