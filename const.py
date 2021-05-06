from os import environ
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

current_dir = Path(__file__).parent.resolve()

load_dotenv(find_dotenv())
CATEGORIES = {
    2: 'IPO', 3: 'FPO',
    5: 'Right Share',
    7: 'Mutual Fund',
    8: 'Debenture'}
ORIGIN = environ['ORIGIN']
API_URL = environ['API_URL']
PDF_URL = environ['PDF_URL']
REFERER = environ['REFERER']
CHANNEL = environ['CHANNEL']
BOT_TOKEN = environ['BOT_TOKEN']
NEWS_URL_ML = environ['NEWS_URL_ML']
NEWS_URL_BM = environ['NEWS_URL_BM']
DATABASE_URI = current_dir / 'nepstonks.db'
BOT_USERNAME = environ['BOT_USERNAME']
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
