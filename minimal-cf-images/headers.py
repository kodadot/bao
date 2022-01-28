# from dotenv import load_dotenv
from os import getenv

# load_dotenv()
ACCOUNT = 'b3f9fdfd827152316d080a5ddee59915'
# ACCOUNT = getenv('ACCOUNT')
API_KEY = getenv('CF_API_KEY')

CF_IMAGES_URI = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/images/v1"
HEADERS={"Authorization": f"Bearer {API_KEY}"}
