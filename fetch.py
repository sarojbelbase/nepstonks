from typing import Dict, List

import requests
from dateutil.parser import parse

from const import API_URL, CATEGORIES, ORIGIN, PDF_URL, REFERER, ALLOTMENT_URL


def scraped_stocks(category_id: int):
    """gets stocks in a raw form within the provided category

    Args:
        category_id (int): the category to be fetched from the available categories
                                    category_id : 2 -> IPO 
                                    category_id : 3 -> FPO
                                    category_id : 5 -> Right Share
                                    category_id : 7 -> Mutual Fund
                                    category_id : 8 -> Debenture

    Returns:
        List[Dict]: returns the stocks in raw form from the given category
    """

    json = {
        "offset": "1",
        "limit": "10",
        "categoryID": category_id,
        "portalID": "1",
        "cultureCode": "en-US",
        "StockSymbol": ""
    }

    headers = {
        'Pragma': 'no-cache',
        'Origin': ORIGIN,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': REFERER,
        'DNT': '1',
    }
    try:
        response = requests.post(API_URL, headers=headers, json=json)
        return response.json()['d']
    except requests.exceptions.ConnectionError as e:
        return print("Looks like the stock API did an oopsie:\n", e)

def alloted_stocks() -> List[Dict]:
    try:
        response = requests.get(ALLOTMENT_URL)
        return response
    except requests.exceptions.ConnectionError as e:
        return print("Looks like the stock API did an oopsie:\n", e)


def latest_stocks() -> List[Dict]:
    from utils import extract_units, get_sharetype
    stocks = []
    for category_id in list(CATEGORIES.keys()):
        for stock in scraped_stocks(category_id):
            data = {
                'company_name': stock['CompanyName'],
                'closing_date': parse(stock['EndDateString']).date(),
                'investment_id': stock['InvestmentID'],
                'issued_by': stock['IssueManager'],
                'pdf_url': PDF_URL + stock['DescriptionPdf'],
                'ratio': stock['Ratio'],
                'opening_date': parse(stock['StartDateString']).date(),
                'stock_id': stock['CategoryID'],
                'scrip': stock['StockSymbol'],
                'stock_type':  get_sharetype(category_id, stock['ShareType']),
                'units': extract_units(stock['ShareType']),
            }
            stocks.append(data)
    return stocks
