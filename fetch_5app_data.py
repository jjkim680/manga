import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MY_SECRET_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")
account_name = os.getenv("5APPS_ACCOUNT_NAME")
if not account_name:
    raise ValueError("No account name found. Please check your .env file.")

url = f'https://storage.5apps.com/jjkim680/cubari/series/'

custom_headers = {
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
}

response = requests.get(url, headers=custom_headers)

print(response)