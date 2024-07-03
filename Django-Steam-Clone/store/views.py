import random

from django.db.models.manager import BaseManager
from django.shortcuts import render
from django.views.generic import View

from games.models import Games
from utils.get_random_assets import get_store_visual_assets


class StorePage(View):
    def get_rand_start(self, games: BaseManager[Games]) -> int:
        return random.randint(1, (len(games) - 12))

    def get_rand_games(self, number_of_games: int, games: BaseManager[Games]):
        rand_games: list[Games] = []
        for _ in range(number_of_games + 1):
            game = random.choice(games)
            rand_games.append(game)
        return rand_games

    def get(self, *args, **kwargs):
        header, background, is_video = get_store_visual_assets()
        all_games = Games.objects.all()
        rand_start = self.get_rand_start(all_games)
        slide_games = all_games[rand_start:rand_start + 12]
        rand_games = self.get_rand_games(5, all_games)

        return render(
            self.request,
            'store/pages/store.html',
            {
                'title': 'Store',
                'header': header,
                'background': background,
                'is_video': is_video,
                'slide_games': slide_games,
                'rand_games': rand_games,
                'slide_len': range(1, (len(slide_games) + 1)),
            }
        )
