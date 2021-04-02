from typing import Dict, List

import requests
from dateutil import parser

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
            'end_date': parser.parse(stock['EndDateString']),
            'investment_id': stock['InvestmentID'],
            'issued_by': stock['IssueManager'],
            'nep_end_date': parser.parse(stock['EndDateNP']),
            'nep_start_date': parser.parse(stock['StartDateNP']),
            'pdf': stock['DescriptionPdf'],
            'ratio': stock['Ratio'],
            'start_date': parser.parse(stock['StartDateString']),
            'stock_id': stock['CategoryID'],
            'stock_symbol': stock['StockSymbol'],
            'stock_type': stock['CategoryName'],
            'units': stock['ShareType'].split(":")[1],
        }
        stocks.append(data)
    return stocks
