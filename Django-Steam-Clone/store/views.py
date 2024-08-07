import math
import random

from django.db.models.manager import BaseManager
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, View

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
        )
        rand_start = self.get_rand_start(deep_disc_games, True)
        return deep_disc_games[rand_start: rand_start + 21]

    def get_random_range_games(
        self, games: BaseManager[Games], qtd_games: int
    ):
        rand_range = random.randint(1, len(games) - qtd_games)
        return games[rand_range:rand_range + qtd_games]

    def get(self, *args, **kwargs):
        header, background, is_video = get_store_visual_assets()
        all_games = Games.objects.all()
        disc_games, is_sale = self.get_slide_games(all_games, is_sale=True)
        rand_start = self.get_rand_start(disc_games, is_sale)
        rand_games = grid_games = top_sellers = under_20_games = None
        deep_disc_games = None

        if is_sale:
            slide_games = disc_games[rand_start:rand_start+24]
            deep_disc_games = self.get_deep_discount_games(all_games, is_sale)
            grid_games = self.get_random_range_games(disc_games, 29)
            top_sellers = self.get_random_range_games(
                all_games.filter(reviews__positive_percent__gt=90), 16
            )
            under_20_games = self.get_random_range_games(
                all_games.filter(price_final__lt=20), 8
            )
        else:
            slide_games = disc_games[rand_start:rand_start+12]
            rand_games = self.get_rand_games(5, slide_games)

        categories_to_browse = Genres.objects.filter(
            id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16],
        )

        return render(
            self.request,
            'store/pages/store.html',
            {
                'site_title': 'Store',
                'header': header,
                'background': background,
                'is_video': is_video,
                'is_sale': is_sale,
                'slide_games': slide_games,
                'rand_games': rand_games,
                'grid_games': grid_games[1:15] if grid_games else None,
                'grid_games2': grid_games[15:29] if grid_games else None,
                'deep_disc_games': deep_disc_games,
                'slide_len': self.get_slide_length(is_sale, slide_games),
                'slide_deep_disc_len': self.get_slide_length(
                    is_sale, deep_disc_games
                ),
                'categories': categories_to_browse,
                'category_slide_len': range(
                    1, math.ceil((len(categories_to_browse) / 4) + 1)
                ),
                'top_sellers': top_sellers,
                'under_20_games': under_20_games,
            }
        )


class AppPage(DetailView):
    model = Games
    template_name = 'store/pages/app.html'
    context_object_name = 'app_details'
    slug_url_kwarg = 'game_slug'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            slug=self.kwargs.get('game_slug'),
            steam_appid=self.kwargs.get('steam_appid')
        ).select_related('reviews')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        game = context.get('app_details')

        context.update({
            'game': game,
            'site_title': game.name if game else None,
        })

        return context
