import time
import random
from cubari_5apps_client import fetch_cubari_data
from weebcentral_client import fetch_slug_from_title, is_read
import platform
import json
import os

def update_manga_data_json():
    # 1. Dynamically find the exact folder this Python script lives in
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 2. Join that folder path with the filename
    save_path = os.path.join(BASE_DIR, 'manga_data.json')

    print(f"Saving data to: {save_path}")

    manga_data = fetch_cubari_data(save_path=save_path)

    for manga_dict in manga_data.values():
        if not manga_dict.get("caught_up"):
            time.sleep(random.uniform(0.5, 3.5))
            manga_dict["read_chapter_count"] = len(manga_dict["chapters"])
            manga_dict.pop("chapters")
            manga_dict["caught_up"] = is_read(manga_dict=manga_dict)
        

    # Saved into json file for webpage to use
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(manga_data, f, ensure_ascii=False, indent=4)
    print("Finished saving manga data")


if __name__ == "__main__":
    update_manga_data_json()
