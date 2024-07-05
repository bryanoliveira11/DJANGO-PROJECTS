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


def get_movies(data):
    if len(data.get('movies')) > 3:
        movie1 = data.get('movies')[0].get('webm').get('480')
        movie2 = data.get('movies')[1].get('webm').get('480')
        movie3 = data.get('movies')[2].get('webm').get('480')
    elif len(data.get('movies')) == 1:
        movie1 = data.get('movies')[0].get('webm').get('480')
        movie2 = movie3 = None
    elif len(data.get('movies')) == 2:
        movie1 = data.get('movies')[0].get('webm').get('480')
        movie2 = data.get('movies')[1].get('webm').get('480')
        movie3 = None

    return movie1, movie2, movie3


def get_prices(data):
    if data.get('price_overview') is not None:
        price_initial = data.get(
            'price_overview').get('initial_formatted')
        price_final = data.get(
            'price_overview').get('final_formatted')
        discount = data.get(
            'price_overview').get('discount_percent')
    else:
        price_initial = price_final = discount = None

    return price_initial, price_final, discount


def get_publishers(data):
    try:
        publishers = data.get('publishers')[1]
    except IndexError:
        publishers = data.get('publishers')[0]

    return publishers


if __name__ == '__main__':
    from games.models import Games

    # for i in range(len(ids_list)):
    try:
        game_id = '377160'
        data = get_single_game_data(game_id)

        if data is not None:
            movie1, movie2, movie3 = get_movies(data)
            price_initial, price_final, discount = get_prices(data)
            publishers = get_publishers(data)

            Games.objects.create(
                name=data.get('name'),
                steam_appid=data.get('steam_appid'),
                is_free=bool(data.get('is_free')),
                short_description=data.get('short_description'),
                sale_image='https://shared.cloudflare.steamstatic.com/'
                f'store_item_assets/steam/apps/{game_id}/library_600x900'
                '_2x.jpg?t=1580240296',
                capsule_image='https://shared.cloudflare.steamstatic.com'
                f'/store_item_assets/steam/apps/{game_id}/capsule_616x353.'
                'jpg?t=1447182531',
                minimum_requirements=data.get(
                    'pc_requirements', '').get('minimum'),
                recommended_requirements=data.get(
                    'pc_requirements', '').get('recommended'),
                developers=data.get('developers')[0],
                publishers=publishers,
                price_initial=price_initial,
                price_final=price_final,
                discount_percent=discount,
                screenshot1=data.get('screenshots')[
                    0].get('path_thumbnail'),
                screenshot2=data.get('screenshots')[
                    1].get('path_thumbnail'),
                screenshot3=data.get('screenshots')[
                    2].get('path_thumbnail'),
                screenshot4=data.get('screenshots')[
                    3].get('path_thumbnail'),
                screenshot5=data.get('screenshots')[
                    4].get('path_thumbnail'),
                background_raw=data.get('background_raw'),
                movie1=movie1,
                movie2=movie2,
                movie3=movie3,
            )

    except (KeyError, AttributeError) as err:
        print(f'Error While Fetching Data in game {game_id}', err)
        # continue
