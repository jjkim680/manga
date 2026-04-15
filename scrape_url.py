import requests
from bs4 import BeautifulSoup
import argparse

def main():
    # initialize parser
    parser = argparse.ArgumentParser(description="manga url scraper")
    # positional arguments
    parser.add_argument("manga_title", help="manga title")

    args = parser.parse_args()
    query = args.manga_title

    # This specific string tells the website: "I am using Chrome version 120 on Windows 10."
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Step 1: The bot goes to the search results page
    search_url = f'https://weebcentral.com/search/data?author=&text={query}&sort=Best%20Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full%20Display'
    response = requests.get(search_url, headers=custom_headers)

    # Step 2: The bot loads the raw HTML code so it can be searched
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 3: The bot finds the exact HTML link tag for the manga. 
    # It looks for an 'a' tag (a link) that has a specific class name.
    manga_link = soup.find("a")

    if manga_link:
        # This grabs the actual URL text: "/series/01J76XYCYJ0P680SKX3QZ0NQD7/Spy-X-Family"
        href_text = manga_link.get("href") 
        
        # Step 4: The bot chops up the URL text wherever there is a '/' symbol
        # This splits it into pieces: ['', 'series', '01J76XYCYJ0P680SKX3QZ0NQD7', 'Spy-X-Family']
        url_parts = href_text.split('/') 
        
        # The ID is the 3rd piece of data in that list (which Python counts as position #2)
        manga_id = url_parts[4] 
        
        print(f"Success! The extracted Manga ID is: {manga_id}")
    else:
        print("Could not find the manga link on this page.")


if __name__ == "__main__":
    main()