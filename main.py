import time
import random
from cubari_5apps_client import fetch_cubari_data
from weebcentral_client import fetch_slug_from_title, is_read
import platform
import json

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
        manga_dict["caught_up"] = is_read(manga_dict=manga_dict)

    # test = [manga_dict.get("caught_up") for manga_dict in manga_data]
    # print(test)

    if platform.system() == 'Linux':
        save_path = '/var/www/html/manga_data.json'
        print(f"Linux detected. Saving to web server at: {save_path}")
    else:
        # os.path.join with os.getcwd() ensures it saves in the same folder it's run from
        save_path = os.path.join(os.getcwd(), 'manga_data.json')
        print(f"Not linux detected. Saving locally at: {save_path}")

    # Saved into json file for webpage to use
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(manga_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    read_manga()
