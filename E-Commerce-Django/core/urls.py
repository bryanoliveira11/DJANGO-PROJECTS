from django.urls import path

from core import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
