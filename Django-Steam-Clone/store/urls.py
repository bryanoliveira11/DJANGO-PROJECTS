from django.urls import path

from store.views import AppPage, StorePage

app_name = 'store'

urlpatterns = [
    path('', StorePage.as_view(), name='store'),
    path(
        'app/<str:steam_appid>/<slug:game_slug>',
        AppPage.as_view(), name='app'
    ),
]
