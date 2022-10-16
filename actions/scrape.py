from json import loads

import requests
from dateutil.parser import parse
from utils import (ALLOTMENT_URL, API_URL, CATEGORIES, PDF_URL, extract_units,
                   get_sharetype, html_scraper, store)


def scrape_stocks():
    """
    gets stocks in a raw form within the list of categories as defined in utils/const.py

    Example:
            category_id : 2 -> IPO 
            category_id : 3 -> FPO
            category_id : 5 -> Right Share
            category_id : 7 -> Mutual Fund
            category_id : 8 -> Debenture

    Stores:
        List[Dict]: stores the stocks in dict form in store.new_stocks

    """

    for category_id in list(CATEGORIES.keys()):

        payload = {
            "offset": "1",
            "limit": "10",
            "categoryID": category_id,
            "portalID": "1",
            "cultureCode": "en-US",
            "StockSymbol": ""
        }

        try:
            response = requests.post(API_URL, json=payload)
            stocks = response.json()['d']

        # If the API is down break the loop and return the stocks
        except requests.exceptions.ConnectionError as e:
            print("Looks like the stock API did an oopsie:\n", e)
            break

        # Append stocks to the list of stocks
        for stock in stocks:
            store.new_stocks.append(
                {
                    'ratio': stock["Ratio"],
                    'scrip': stock['StockSymbol'],
                    'stock_id': stock['CategoryID'],
                    'issued_by': stock['IssueManager'],
                    'company_name': stock['CompanyName'],
                    'investment_id': stock['InvestmentID'],
                    'units': extract_units(stock['ShareType']),
                    'pdf_url': PDF_URL + stock['DescriptionPdf'],
                    'closing_date': parse(stock['EndDateString']).date(),
                    'opening_date': parse(stock['StartDateString']).date(),
                    'stock_type':  get_sharetype(category_id, stock['ShareType'])
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
