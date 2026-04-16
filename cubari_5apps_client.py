import os
import time
import random
from dotenv import load_dotenv
from api_client import fetch_data

def get_dotenv():
    load_dotenv()

    account_name = os.getenv("5APPS_ACCOUNT_NAME")
    if not account_name:
        raise ValueError("No account name found. Please check your .env file.")

    api_token = os.getenv("MY_SECRET_API_TOKEN")
    if not api_token:
        raise ValueError("No API token found. Please check your .env file.")
    
    return account_name, api_token    


def fetch_series_data(account_name: str, headers: dict) -> dict:
    url = f'https://storage.5apps.com/{account_name}/cubari/series/'
    response = fetch_data(url, headers)

    if response is None:
        print("Failed to fetch data, returning empty dictionary")
        return {}
    
    return response.json().get("items")


def filter_manga_data(manga_data: dict) -> dict:
    keys_to_keep = ['slug', 'coverUrl', 'title', 'chapters']
    filtered_manga_data = {k: manga_data.get(k, []) for k in keys_to_keep if k in manga_data}
    return filtered_manga_data


def fetch_manga_data(account_name: str, headers: dict, manga_code: str) -> dict:
    url = f'https://storage.5apps.com/{account_name}/cubari/series/{manga_code}'
    response = fetch_data(url, headers)

    if response is None:
        print("Failed to fetch data, returning empty dictionary")
        return {}

    return filter_manga_data(response.json())


def fetch_cubari_data() -> dict:
    global manga_data

    ACCOUNT_NAME, API_TOKEN = get_dotenv()

    headers = {
        "authorization": f"Bearer {API_TOKEN}",
        "origin": "https://cubari.moe",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
    }

    # Fetch series data, then for each series, fetch its manga data, and use that data to fill in manga_data
    series_data = fetch_series_data(ACCOUNT_NAME, headers)
    manga_keys = list(series_data.keys())
    manga_data = dict()

    for manga_key in manga_keys:
        time.sleep(random.uniform(0.5, 3.5))
        manga_data[manga_key] = fetch_manga_data(ACCOUNT_NAME, headers, manga_code=manga_key)
        print(f"Fetched manga data for: {manga_data.get(manga_key).get('title')}")

    print("Finished fetching manga data")
    return manga_data
    
    
if __name__ == "__main__":
    fetch_cubari_data()