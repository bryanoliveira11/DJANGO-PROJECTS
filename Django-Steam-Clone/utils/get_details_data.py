# flake8:noqa

import os
import sys
from pathlib import Path

import django
import requests
from django.conf import settings
from django.utils.text import slugify
from steam_utils_data import genres_image_url, ids_list
from unidecode import unidecode

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
    if not data:
        return None
    return data[id]['data']


def get_movies(data):
    movie1 = None
    movie2 = None
    movie3 = None

    if data is None or data.get('movies') is None:
        return movie1, movie2, movie3

    if len(data.get('movies')) > 3:
        movie1 = data.get('movies')[0].get('webm').get('480')
        movie2 = data.get('movies')[1].get('webm').get('480')
        movie3 = data.get('movies')[2].get('webm').get('480')
    elif len(data.get('movies')) == 1:
        movie1 = data.get('movies')[0].get('webm').get('480')
    elif len(data.get('movies')) == 2:
        movie1 = data.get('movies')[0].get('webm').get('480')
        movie2 = data.get('movies')[1].get('webm').get('480')

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


def get_developers(data):
    if data is None or data.get('developers') is None:
        return None
    return data.get('developers')[0]


def get_genres(data):
    from games.models import Genres

    if data is None:
        return

    genres_data = data.get('genres')

    if genres_data is None:
        return

    genres_db_list = []

    for i in range(len(genres_data)):
        genre_name = genres_data[i].get('description')
        genre_db = Genres.objects.filter(name=genre_name).first()
        if not genre_db:
            genre_db = Genres.objects.create(name=genre_name)
        genres_db_list.append(genre_db)

    return genres_db_list


def get_details_data():
    from games.models import Games

    for i in range(len(ids_list)):
        try:
            game_id = ids_list[i]
            data = get_single_game_data(game_id)

            if data is not None:
                movie1, movie2, movie3 = get_movies(data)
                price_initial, price_final, discount = get_prices(data)
                publishers = get_publishers(data)
                game = Games.objects.create(
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
                    developers=get_developers(data),
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
                db_genres = get_genres(data)
                if db_genres:
                    for i in range(len(db_genres)):
                        genre = db_genres[i]
                        game.genres.add(genre)
        except (KeyError, AttributeError, TypeError) as err:
            print(f'Error While Fetching Data in game {game_id}', err)
            continue


def update_details_with_reviews():
    from games.models import Games, Reviews

    all_games = Games.objects.all()

    for i in range(len(all_games)):
        steam_id = all_games[i].steam_appid
        reviews_url = f'https://store.steampowered.com/appreviews/{
            steam_id}?json=1'
        data = requests.get(reviews_url).json().get('query_summary')
        description = data.get('review_score_desc')
        total_reviews = data.get('total_reviews')
        positive_reviews = data.get('total_positive')
        negative_reviews = data.get('total_negative')
        review = Reviews.objects.create(
            description=description,
            total_reviews=total_reviews,
            total_positive=positive_reviews,
            total_negative=negative_reviews,
        )
        game = Games.objects.filter(steam_appid=steam_id).first()
        if game and not game.reviews:
            game.reviews = review
            game.save()


def calculate_review_percent():
    from django.contrib.humanize.templatetags.humanize import intcomma

    from games.models import Reviews

    reviews = Reviews.objects.all()

    for i in range(len(reviews)):
        review = reviews[i]

        if review.total_positive and review.total_reviews:
            positive_percent = (
                (review.total_positive * 100) / review.total_reviews
            )
            review.positive_percent = positive_percent
            review.save()


def update_genres_with_images():
    from games.models import Genres
    genres_to_update = Genres.objects.filter(
        id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16],
    )
    for i in range(len(genres_to_update)):
        genre = genres_to_update[i]
        genre.image_url = genres_image_url[i]
        genre.save()


def remove_currency_from_prices():
    from games.models import Games

    def replace_currency(value: str):
        return value.replace('R$', '').replace(' ', '')

    games = Games.objects.filter(
        price_initial__icontains='R$',
        price_final__icontains='R$',
    )
    for i in range(len(games)):
        game = games[i]
        if game.price_initial and game.price_final:
            game.price_initial = replace_currency(game.price_initial)
            game.price_final = replace_currency(game.price_final)
            game.save()


def generate_slug_from_game_name():
    from games.models import Games

    def custom_slugify(value):
        value = unidecode(value)
        return slugify(value)

    games = Games.objects.all()
    for i in range(len(games)):
        game = games[i]
        if game:
            game.slug = custom_slugify(game.name)
            game.save()


def update_details_with_background():
    from games.models import Games

    all_games = Games.objects.all()

    for i in range(len(all_games)):
        steam_id = all_games[i].steam_appid
        data = get_single_game_data(steam_id)
        if data:
            background = data.get('background')
            game = all_games[i]
            game.background = background
            game.save()


def update_details_with_app_page_content():
    from games.models import Games

    all_games = Games.objects.all()

    for i in range(len(all_games)):
        steam_id = all_games[i].steam_appid
        data = get_single_game_data(steam_id)
        if data:
            required_age = data.get('required_age', None)
            release_date = data.get('release_date', {}).get('date', None)
            controller_support = data.get('controller_support', None)
            metacritic_score = data.get('metacritic', {}).get('score', None)
            metacritic_url = data.get('metacritic', {}).get('url', None)
            about_the_game = data.get('about_the_game', None)
            languages = data.get('supported_languages', None)
            app_reviews = data.get('reviews', None)
            legal_notice = data.get('legal_notice', None)
            ratings = data.get('ratings', None)
            pegi_rating = None

            if ratings:
                pegi = ratings.get('pegi', None)
                if pegi:
                    pegi_rating = pegi.get('descriptors', None)

            game = all_games[i]
            game.required_age = required_age
            game.release_date = release_date
            game.controller_support = controller_support
            game.metacritic_score = metacritic_score
            game.metacritic_url = metacritic_url
            game.about_the_game = about_the_game
            game.languages = languages
            game.app_reviews = app_reviews
            game.legal_notice = legal_notice
            game.pegi_rating = pegi_rating
            game.save()


def update_currently_popular():
    from games.models import Games

    all_games = Games.objects.all()

    for i in range(len(all_games)):
        game = all_games[i]
        if game.reviews:
            reviews = game.reviews
            if reviews.positive_percent is not None and reviews.total_reviews is not None:
                if reviews.positive_percent > 85 and reviews.total_reviews > 15000:
                    game.currently_popular = True
                    game.save()


if __name__ == '__main__':
    # get_details_data()
    # update_details_with_reviews()
    # calculate_review_percent()
    # update_genres_with_images()
    # remove_currency_from_prices()
    # generate_slug_from_game_name()
    # update_details_with_background()
    # update_details_with_app_page_content()
    update_currently_popular()
