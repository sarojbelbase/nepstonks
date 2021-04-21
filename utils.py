import re
from datetime import date
from unicodedata import normalize

import requests
from nepali_datetime import date as nepdate


def bleach(given_text: str) -> str:
    extra_space = normalize('NFKD', given_text)
    return extra_space.replace('\n', '')


def fix_last_dharko(given_text: str) -> str:
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


def pdf_url_resolves(pdf: str) -> bool:
    from const import PDF_URL
    """Checks if the given pdf resolves (if it has pdf)

    Args:
        pdf (str): pdf filename with pdf extension

    Returns:
        bool: returns False if it can't resolve the generated pdf link
         from the given pdf else returns True
    """
    if pdf:
        pdf_url = PDF_URL + pdf
        request = requests.get(pdf_url)
        return True if request.status_code == 200 else False
    else:
        return False


def handle_response(the_url, payload):
    try:
        response = requests.post(the_url, data=payload)
        response.raise_for_status()
        return print(response.content.decode())
    except requests.exceptions.HTTPError as error:
        return print(error.response.text)
