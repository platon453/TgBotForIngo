import os
from dotenv import load_dotenv

load_dotenv()

VK_API_TOKEN = os.getenv("VK_API_TOKEN")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")
LANDING_URL = os.getenv("LANDING_URL", "https://www.ingos.ru/internship/")
