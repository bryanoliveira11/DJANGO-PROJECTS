# flake8:noqa

import requests
from steam_popular_ids import ids_list

GAME_ID = ''


def get_api_url(id: str):
    url = f'https://store.steampowered.com/api/appdetails?appids={id}'
    return url


def get_single_game_data(id: str):
    url = get_api_url(id)
    data = requests.get(url).json()
    return data or None


print(get_single_game_data(ids_list[5]))
