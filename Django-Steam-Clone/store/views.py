import math
import random

from django.db.models.manager import BaseManager
from django.shortcuts import render
from django.views.generic import View

from games.models import Games
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
        rand_start = self.get_rand_start(games, is_sale)

        # off sale, games = 12 in total, 12 slides
        if not is_sale:
            slide_games = games[rand_start:rand_start + 12]
            return slide_games, is_sale

        # on sale, games = 24 in total, 3 per slide, 8 slides
        slide_games = games[rand_start: rand_start + 24]
        return slide_games, is_sale

    def get_slide_length(self, is_sale: bool, slide_games: BaseManager[Games]):
        slide_len = range(1, (len(slide_games) + 1))

        if is_sale:
            slide_len = range(1, math.floor((len(slide_games) / 3)) + 1)

        return slide_len

    def get(self, *args, **kwargs):
        header, background, is_video = get_store_visual_assets()
        all_games = Games.objects.all()
        rand_games = self.get_rand_games(5, all_games)
        slide_games, is_sale = self.get_slide_games(all_games, True)

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
                'slide_len': self.get_slide_length(is_sale, slide_games),
            }
        )
