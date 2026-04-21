import time
import random
from cubari_5apps_client import fetch_cubari_data
from weebcentral_client import fetch_slug_from_title, is_read

def read_manga():
    manga_titles = []
    # manga_covers = []
    unread = []

    # title = input("Type title")
    # code = fetch_slug_from_title(title)
    # print(code)

    manga_data = fetch_cubari_data()

    for manga_dict in manga_data.values():
        time.sleep(random.uniform(0.5, 3.5))
        manga_titles.append(manga_dict.get("title"))
        if is_read(manga_dict=manga_dict):
            unread.append(0)
        else:
            unread.append(1)

    print(manga_titles)
    print(unread)

if __name__ == "__main__":
    read_manga()
