import requests
from dateutil.parser import parse

from utils import ALLOTMENT_URL, API_URL, html_scraper, store


def scrape_stocks():

    params = {
        "pageNo": 1,
        "itemsPerPage": 10,
        "pagePerDisplay": 5
    }

    try:
        response = requests.get(API_URL, params=params)
        json_result = response.json()
        stocks = json_result.get("result", {}).get("data", [])

    # If the API is down break the loop and return the stocks
    except requests.exceptions.ConnectionError as e:
        print("Looks like the stock API did an oopsie:\n", e)

    # Append stocks to the list of stocks

    for stock in stocks:
        store.new_stocks.append(
            {
                'id': stock['ipoId'],
                'company_name': stock['companyName'],
                'stock_symbol': stock['stockSymbol'],
                'share_registrar': stock['shareRegistrar'],
                'sector_name': stock['sectorName'],
                'share_type': stock['shareType'],
                'price_per_unit': stock['pricePerUnit'],
                'rating': stock['rating'],
                'units': stock['units'],
                'min_units': stock['minUnits'],
                'max_units': stock['maxUnits'],
                'total_amount': stock['totalAmount'],
                'opening_date': parse(stock['openingDateAD']).date(),
                'closing_date': parse(stock['closingDateAD']).date(),
                'fiscal_year': stock['fiscalYearAD']
            }
        )


def scrape_announcements():
    """
    Scrapes the announcements from the allotment page provided in utils/const.py

    Stores:
        List[Dict]: stores the announcements in dict form in store.new_announcements

    """

    whole_html = html_scraper(ALLOTMENT_URL)
    area = whole_html.find("div", {"class": "announcement-list"})

    announcements = area.find_all(
        "div", {"class": "featured-news-list"}
    )

    for announcement in announcements:
        content_url = announcement.find("a")['href']

        content = announcement.find(
            "h4", {"class": "featured-announcement-title"}
        )

        date = announcement.find(
            "span", {"class": "text-org"}
        )

        store.new_announcements.append(
            {
                'content': content.text.strip(),
                'content_url': content_url.strip(),
                'published_date': parse(date.text.strip()).date()
            }
        )
