# flake8:noqa

import requests
from steam_popular_ids import ids_list


def get_api_url(id: str):
    url = f'https://store.steampowered.com/api/appdetails?appids={
        id}&l=english'
    return url


def get_single_game_data(id: str):
    url = get_api_url(id)
    data = requests.get(url).json()
    return data[id]['data']


def get_necessary_data(data):
    if data is None:
        return

    publishers = data.get('publishers')[1]

    if not publishers:
        publishers = data.get('publishers')[0]

    new_data = {
        'name': data.get('name'),
        'steam_appid': data.get('steam_appid'),
        'short_description': data.get('short_description'),
        'header_image': data.get('header_image'),
        'minimum_requirements': data.get('pc_requirements', '').get('minimum'),
        'recommended_requirements': data.get('pc_requirements', '').get('recommended'),
        'developers': data.get('developers')[0],
        'publishers': publishers,
        'price': data.get('price_overview').get('final_formatted'),
        'screenshot1': data.get('screenshots')[0].get('path_thumbnail'),
        'screenshot2': data.get('screenshots')[1].get('path_thumbnail'),
        'screenshot3': data.get('screenshots')[2].get('path_thumbnail'),
        'screenshot4': data.get('screenshots')[3].get('path_thumbnail'),
        'background_raw': data.get('background_raw'),
    }

    return new_data


data = get_single_game_data('1245620')
new_data = get_necessary_data(data)
print(new_data)
