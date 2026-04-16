import time
import random
from cubari_5apps_client import fetch_cubari_data
from weebcentral_client import fetch_slug_from_title, is_read

# title = input("Type title")
# code = fetch_slug_from_title(title)
# print(code)

not_caught_up = []
caught_up = []

manga_data = fetch_cubari_data()
for manga_dict in manga_data.values():
    time.sleep(random.uniform(0.5, 3.5))
    if is_read(manga_dict=manga_dict):
        caught_up.append(manga_dict.get("title"))
    else:
        not_caught_up.append(manga_dict.get("title"))

print(not_caught_up)
print(caught_up)