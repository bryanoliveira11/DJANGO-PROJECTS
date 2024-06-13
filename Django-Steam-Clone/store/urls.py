from django.urls import path

from store.views import StorePage

app_name = 'store'

urlpatterns = [
    path('', StorePage.as_view(), name='store')
]
