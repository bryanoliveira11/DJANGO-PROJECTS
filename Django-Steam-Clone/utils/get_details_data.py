# flake8:noqa

import os
import sys
from pathlib import Path

import django
import requests
from django.conf import settings
from steam_popular_ids import ids_list

DJANGO_BASE_DIR = Path(__file__).parent.parent

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'SteamClone.settings'
settings.USE_TZ = False

django.setup()


def get_api_url(id: str):
    url = f'https://store.steampowered.com/api/appdetails?appids={
        id}&l=english'
    return url


def get_single_game_data(id: str):
    url = get_api_url(id)
    data = requests.get(url).json()
    return data[id]['data']


if __name__ == '__main__':
    from games.models import Games

    for i in range(len(ids_list)):
        try:
            game_id = ids_list[i]
            data = get_single_game_data(game_id)

            if data is not None:
                try:
                    publishers = data.get('publishers')[1]
                    price = data.get('price_overview').get('final_formatted')
                except IndexError:
                    publishers = data.get('publishers')[0]
                    price = None

                Games.objects.create(
                    name=data.get('name'),
                    steam_appid=data.get('steam_appid'),
                    short_description=data.get('short_description'),
                    header_image=data.get('header_image'),
                    minimum_requirements=data.get(
                        'pc_requirements', '').get('minimum'),
                    recommended_requirements=data.get(
                        'pc_requirements', '').get('recommended'),
                    developers=data.get('developers')[0],
                    publishers=publishers,
                    price=price,
                    screenshot1=data.get('screenshots')[
                        0].get('path_thumbnail'),
                    screenshot2=data.get('screenshots')[
                        1].get('path_thumbnail'),
                    screenshot3=data.get('screenshots')[
                        2].get('path_thumbnail'),
                    screenshot4=data.get('screenshots')[
                        3].get('path_thumbnail'),
                    background_raw=data.get('background_raw'),
                )

        except (KeyError, AttributeError) as err:
            print(f'Error While Fetching Data in game {game_id}', err)
            continue
