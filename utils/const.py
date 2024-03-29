from os import environ
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

current_dir = Path(__file__).parent.parent.resolve()

load_dotenv(find_dotenv())

API_URL = environ['API_URL']
CHANNEL = environ['CHANNEL']
BOT_TOKEN = environ['BOT_TOKEN']
BOT_USERNAME = environ['BOT_USERNAME']
ALLOTMENT_URL = environ['ALLOTMENT_URL']
DATABASE_URI = current_dir / 'nepstonks.db'
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
