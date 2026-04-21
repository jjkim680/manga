from bs4 import BeautifulSoup
import numpy as np
from bs4 import BeautifulSoup
from api_client import fetch_data


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_slug_from_title(query):
    url = f'https://weebcentral.com/search/data?author=&text={query}&sort=Best%20Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full%20Display'
    response = fetch_data(url=url, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")
    manga_link = soup.find("a")

    if manga_link:
        # href_text = 'https://weebcentral.com/series/01J76XYFPF0C74JMR2H1MTQ2MR/Look-Back'
        href_text = manga_link.get("href") 
        
        # Split url into pieces
        # url_parts = ['https:', '', 'weebcentral.com', 'series', '01J76XYFPF0C74JMR2H1MTQ2MR', 'Look-Back']
        url_parts = href_text.split('/') 
        
        # The ID is the 5th piece of data in that list (which Python counts as position #4)
        # '01J76XYFPF0C74JMR2H1MTQ2MR'
        manga_id = url_parts[4] 
        
        print(f"Success! The extracted Manga ID is: {manga_id}")
    else:
        print("Could not find the manga link on this page.")


def is_read(manga_dict):
    slug = manga_dict.get('slug')
    url = f'https://weebcentral.com/series/{slug}/full-chapter-list'
    response = fetch_data(url=url, headers=HEADERS)

    # manga_dict['chapters'] = ['85', '84', '83'...]
    local_chapters = manga_dict.get("chapters", [])

    # Find highest read index or return 0
    if local_chapters:
        highest_read_index = np.array(local_chapters).astype(int).max()
    else:
        highest_read_index = 0


    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This selector targets every chapter link on the page
    remote_links = soup.select('a[href^="https://weebcentral.com/chapters/"]')
    
    # The total number of links IS the absolute index for the latest chapter
    total_remote_chapters = len(remote_links)
    
    # Compare
    if total_remote_chapters > highest_read_index:
        return False
    else:
        return True
    

if __name__ == "__main__":
    title = "one punch man"
    fetch_slug_from_title(title)
    # is_read()