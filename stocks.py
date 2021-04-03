from datetime import datetime
from typing import Dict, List

import requests
from dateutil.parser import parse
from nepali_datetime import date

from const import API_URL, ORIGIN, REFERER


def fetch_latest_stocks(category_id: int) -> List[Dict]:
    """Fetches latest stocks 20 stocks with given category

    Args:
        category_id (int): the category to be fetched from the available categories
                                        IPO -> category_id : 2
                                        FPO -> category_id : 3
                                        Right Share -> category_id : 5
                                        Mutual Fund -> category_id : 7
                                        Debenture -> category_id : 8

    Returns:
        List[Dict]: returns the lastes ipos of the given category
    """

    json = {
        "offset": "1",
        "limit": "20",
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
    raw_stocks = response.json()['d']
    stocks = []
    for stock in raw_stocks:
        data = {
            'company_name': stock['CompanyName'],
            'end_date': parse(stock['EndDateString']).date(),
            'investment_id': stock['InvestmentID'],
            'issued_by': stock['IssueManager'],
            'nep_end_date': to_nepali_date(stock['EndDateString']),
            'nep_start_date': to_nepali_date(stock['StartDateString']),
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


def get_units(sharetype: str) -> str:
    index = sharetype.find(':')
    if index != -1:
        return sharetype[index+1:].strip()


def to_nepali_date(givendate):
    return date.from_datetime_date(parse(givendate).date())
