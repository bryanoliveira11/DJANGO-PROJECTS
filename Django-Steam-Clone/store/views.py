import random

from django.shortcuts import render
from django.views.generic import View

from games.models import Games


class StorePage(View):
    def get(self, *args, **kwargs):
        all_games = Games.objects.all()
        rand_start = random.randint(1, len(all_games))
        rand_price = random.randint(10, 250)
        slide_games = all_games[rand_start:rand_start + 12]

        return render(
            self.request,
            'store/pages/store.html',
            {
                'title': 'Store',
                'slide_games': slide_games,
                'slide_len': range(len(slide_games) - 1),
                'rand_price': f'R$ {rand_price},99',
            }
        )
