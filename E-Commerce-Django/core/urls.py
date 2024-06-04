from django.urls import path

from core import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='home')
]
