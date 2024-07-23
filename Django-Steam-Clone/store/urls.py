from django.urls import path

from store.views import StorePage

app_name = 'store'

urlpatterns = [
    path('', StorePage.as_view(), name='store'),
    path(
        'app/<int:steam_id>/<slug:game_name>',
        StorePage.as_view(), name='app'
    ),
]
