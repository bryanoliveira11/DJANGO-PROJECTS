from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render

from .models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(
        request,
        'core/pages/home.html',
        context={
            'site_title': 'Shop List',
            'products': products,
        }
    )


def login_user(request):
    return render(
        request,
        'core/pages/login.html',
        context={
            'site_title': 'Login',
        }
    )


def logout_user(request):
    return HttpResponse()
