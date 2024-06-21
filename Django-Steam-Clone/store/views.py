from django.shortcuts import render
from django.views.generic import View

from games.models import Games


class StorePage(View):
    def get(self, *args, **kwargs):
        all_games = Games.objects.all()
        slide_games = all_games[:12]

        return render(
            self.request,
            'store/pages/store.html',
            {
                'title': 'Store',
                'slide_games': slide_games,
                'slide_len': range(len(slide_games) - 1),
            }
        )
