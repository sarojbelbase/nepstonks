from typing import Dict, List

import requests
from dateutil.parser import parse

from const import API_URL, CATEGORIES, ORIGIN, REFERER


def get_units(sharetype: str) -> str:
    index = sharetype.find(':')
    if index != -1:
        # get only kittas/units and slice out the "share_type"
        return sharetype[index+1:].strip()


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

    response = requests.post(API_URL, headers=headers, json=json)
    return response.json()['d']


def latest_stocks() -> List[Dict]:
    stocks = []
    for category_id in CATEGORIES:
        for stock in scraped_stocks(category_id):
            data = {
                'company_name': stock['CompanyName'],
                'end_date': parse(stock['EndDateString']).date(),
                'investment_id': stock['InvestmentID'],
                'issued_by': stock['IssueManager'],
                'pdf': stock['DescriptionPdf'],
                'ratio': stock['Ratio'],
                'start_date': parse(stock['StartDateString']).date(),
                'stock_id': stock['CategoryID'],
                'stock_symbol': stock['StockSymbol'],
                'stock_type': stock['CategoryName'],
                'units': get_units(stock['ShareType']),
            }
            stocks.append(data)
    return stocks
