from os import environ
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

current_dir = Path(__file__).parent.resolve()

load_dotenv(find_dotenv())
ORIGIN = environ['ORIGIN']
API_URL = environ['API_URL']
REFERER = environ['REFERER']
CHANNEL = environ['CHANNEL']
BOT_TOKEN = environ['BOT_TOKEN']
BOT_USERNAME = environ['BOT_USERNAME']
DATABASE_URI = current_dir / 'stock.db'
