import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LANDING_URL = os.getenv("LANDING_URL", "https://www.ingos.ru/internship/")
