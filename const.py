from os import environ
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

current_dir = Path(__file__).parent.resolve()

load_dotenv(find_dotenv())
ORIGIN = environ['ORIGIN']
CATEGORIES = [2, 3, 5, 7, 8]
API_URL = environ['API_URL']
REFERER = environ['REFERER']
CHANNEL = environ['CHANNEL']
BOT_TOKEN = environ['BOT_TOKEN']
DATABASE_URI = current_dir / 'stock.db'
BOT_USERNAME = environ['BOT_USERNAME']
HORI_LINE = "-----------------------------------------------"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
