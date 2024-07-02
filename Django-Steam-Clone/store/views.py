import random

from django.shortcuts import render
from django.views.generic import View

from games.models import Games


class StorePage(View):
    def get_rand_start(self, games) -> int:
        return random.randint(1, (len(games) - 12))

    def get(self, *args, **kwargs):
        all_games = Games.objects.all()
        rand_start = self.get_rand_start(all_games)
        slide_games = all_games[rand_start:rand_start + 12]

        return render(
            self.request,
            'store/pages/store.html',
            {
                'title': 'Store',
                'slide_games': slide_games,
                'slide_len': range(1, (len(slide_games) + 1)),
            }
        )
