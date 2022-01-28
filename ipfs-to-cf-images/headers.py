from dotenv import load_dotenv
from os import getenv

load_dotenv()
ACCOUNT = getenv('ACCOUNT')
API_KEY = getenv('API_KEY')

CF_IMAGES_URI = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/images/v1"
HEADERS={"Authorization": f"Bearer {API_KEY}"}