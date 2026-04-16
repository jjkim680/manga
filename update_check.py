import re
import requests
from bs4 import BeautifulSoup
from get_manga_data import fetch_cubari_data
import numpy as np

custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

not_caught_up = []
caught_up = []

def check_manga_update(manga_dict):
    slug = manga_dict.get('slug')
    title = manga_dict.get('title')
    search_url = f'https://weebcentral.com/series/{slug}/full-chapter-list'
    response = requests.get(search_url, headers=custom_headers)

    # --- 1. Get your Local High Water Mark ---
    # manga_dict['chapters'] = ['85', '84', '83'...]
    local_chapters = manga_dict.get("chapters", [])

    if local_chapters:
        # Vectorized conversion of string-integers to actual ints to find the max
        highest_read_index = np.array(local_chapters).astype(int).max()
    else:
        highest_read_index = 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This selector targets every chapter link on the page
        # Based on your screenshot, this is the most reliable way to 'count' releases
        remote_links = soup.select('a[href^="https://weebcentral.com/chapters/"]')
        
        # The total number of links IS the absolute index for the latest chapter
        total_remote_chapters = len(remote_links)
        


        # --- 3. The Final Comparison ---
        if total_remote_chapters > highest_read_index:
            diff = total_remote_chapters - highest_read_index
            print(f"🔔 Update Found!")
            print(f"   Latest Release Index: {total_remote_chapters}")
            print(f"   Your Last Read Index: {highest_read_index}")
            print(f"   You have {diff} unread release(s)!")
            
            not_caught_up.append(manga_dict.get('title'))
        else:
            print("✅ You are all caught up.")
            caught_up.append(manga_dict.get('title'))


manga_data = fetch_cubari_data()
for manga_dict in manga_data.values():
    check_manga_update(manga_dict)

print(not_caught_up)
print(caught_up)