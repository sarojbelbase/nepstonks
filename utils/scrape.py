import requests
from dateutil.parser import parse

from utils import store
from utils.const import API_URL, CATEGORIES, PDF_URL
from utils.helpers import extract_units, get_sharetype


def scraped_stocks():
    """
    gets stocks in a raw form within the list of categories as defined in utils/const.py

    Example:
            category_id : 2 -> IPO 
            category_id : 3 -> FPO
            category_id : 5 -> Right Share
            category_id : 7 -> Mutual Fund
            category_id : 8 -> Debenture

    Returns:
        List[Dict]: returns the stocks in raw form from the given category

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
            stock = response.json()['d']

        # If the API is down break the loop and return the stocks
        except requests.exceptions.ConnectionError as e:
            print("Looks like the stock API did an oopsie:\n", e)
            break

        # Append stocks to the list of stocks
        store.new_stocks.append(
            {
                'ratio': stock['Ratio'],
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
