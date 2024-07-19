import math
import random

from django.db.models import Q
from django.db.models.manager import BaseManager
from django.shortcuts import render
from django.views.generic import View

from games.models import Games, Genres
from utils.get_random_assets import get_store_visual_assets


class StorePage(View):
    def get_rand_start(self, games: BaseManager[Games], is_sale: bool) -> int:
        if not is_sale:
            return random.randint(1, (len(games) - 12))

        # 24 games when it's is sale
        return random.randint(1, (len(games) - 24))

    def get_rand_games(self, number_of_games: int, games: BaseManager[Games]):
        rand_games: list[Games] = []
        for _ in range(number_of_games + 1):
            game = random.choice(games)
            rand_games.append(game)
        return rand_games

    def get_slide_games(
        self, games: BaseManager[Games], is_sale=False
    ) -> tuple[BaseManager[Games], bool]:

        if is_sale:
            games = Games.objects.filter(
                discount_percent__isnull=False,
                discount_percent__gt=0,
                price_initial__icontains='R$',
            ).prefetch_related('genres').select_related('reviews')

        return games, is_sale

    def get_slide_length(
        self, is_sale: bool,
        slide_games: BaseManager[Games] | BaseManager[Genres] | None
    ):
        if not slide_games:
            return

        slide_len = range(1, (len(slide_games) + 1))

        if is_sale:
            slide_len = range(1, math.floor((len(slide_games) / 3)) + 1)

        return slide_len

    def get_deep_discount_games(
        self, games: BaseManager[Games], is_sale: bool
    ):
        if not is_sale:
            return

        deep_disc_games = games.filter(
            discount_percent__isnull=False,
            discount_percent__gt=84,
            price_initial__icontains='R$',
        )
        rand_start = self.get_rand_start(deep_disc_games, True)
        return deep_disc_games[rand_start: rand_start + 21]

    def get(self, *args, **kwargs):
        header, background, is_video = get_store_visual_assets()
        all_games = Games.objects.all()
        disc_games, is_sale = self.get_slide_games(all_games, is_sale=True)
        rand_start = self.get_rand_start(disc_games, is_sale)

        if is_sale:
            slide_games = disc_games[rand_start:rand_start+24]
        else:
            slide_games = disc_games[rand_start:rand_start+12]

        rand_games = self.get_rand_games(5, slide_games)
        grid_games = disc_games[rand_start:rand_start+29]
        deep_disc_games = self.get_deep_discount_games(all_games, is_sale)
        categories_to_browse = Genres.objects.filter(
            id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16],
        )
        top_sellers = all_games.filter(
            Q
            (
                Q(reviews__positive_percent__gt=90) &
                Q(price_initial__icontains='R$') |
                Q(price_initial__isnull=True),
            )
        )
        top_rand_start = random.randint(1, len(top_sellers) - 16)

        return render(
            self.request,
            'store/pages/store.html',
            {
                'title': 'Store',
                'header': header,
                'background': background,
                'is_video': is_video,
                'is_sale': is_sale,
                'slide_games': slide_games,
                'rand_games': rand_games,
                'grid_games': grid_games[1:15],
                'grid_games2': grid_games[15:29],
                'deep_disc_games': deep_disc_games,
                'slide_len': self.get_slide_length(is_sale, slide_games),
                'slide_deep_disc_len': self.get_slide_length(
                    is_sale, deep_disc_games
                ),
                'categories': categories_to_browse,
                'category_slide_len': range(
                    1, math.ceil((len(categories_to_browse) / 4) + 1)
                ),
                'top_sellers': top_sellers[top_rand_start:top_rand_start + 16],
            }
        )
