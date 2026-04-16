import os
import json
import requests
from dotenv import load_dotenv
import numpy as np
import pandas as pd

CACHE_FILENAME = "my_data_cache.json"

def get_headers():
    # check variables from .env
    load_dotenv()
    api_key = os.getenv("MY_SECRET_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please check your .env file.")
    account_name = os.getenv("5APPS_ACCOUNT_NAME")
    if not account_name:
        raise ValueError("No account name found. Please check your .env file.")
    
    custom_headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0",
        "Origin": "https://cubari.moe"
    }

    return custom_headers

def fetch_5apps_cubari_data():
    # check cache existence
    if os.path.exists(CACHE_FILENAME):
        print(f'Found {CACHE_FILENAME}! Loading data from local file...')

        with open(CACHE_FILENAME, 'r') as file:
            return json.load(file)
    
    print("No local cache found. Fetching from the internet...")

    # fetch data
    url = f'https://storage.5apps.com/{account_name}/cubari/series/'

    custom_headers = get_headers()
    response = requests.get(url, headers=custom_headers)

    # response handling
    if response.status_code == 200:
        print("Success!")
        data = response.json().get("items")
        print(data)

        with open(CACHE_FILENAME, 'w') as file:
            json.dump(data, file, indent=4)

        return data
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)


def fetch_manga_data(manga_code):
    url = f'https://storage.5apps.com/jjkim680/cubari/series/{manga_code}'

    headers = get_headers()
    file_response = requests.get(url, headers=headers)
    
    if file_response.status_code == 200:
        # my_reading_history[filename] = file_response.json()
        print(f"Downloaded: {manga_code}")

        data = file_response.json()

        keys_to_keep = ['slug', 'coverUrl', 'title', 'chapters']

        filtered_data = {k: data[k] for k in keys_to_keep if k in data}

        return filtered_data
    else:
        print(f"Failed to download: {manga_code} (Status: {file_response.status_code})")

def fetch_cubari_data():
    global manga_data
    data = fetch_5apps_cubari_data()

    manga_keys = list(data.keys())

    manga_data = dict()

    for manga_key in manga_keys:
        manga_data[manga_key] = fetch_manga_data(manga_key)

    return manga_data
    
if __name__ == "__main__":
    fetch_cubari_data()