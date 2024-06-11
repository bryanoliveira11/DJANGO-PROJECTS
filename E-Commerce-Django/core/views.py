from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from core.forms import SignUpForm

from .models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(
        request,
        'core/pages/home.html',
        context={
            'site_title': 'Shop List',
            'header_title': 'Django-Commerce',
            'header_subtitle': 'List of Products.',
            'products': products,
        }
    )


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'You are logged in.')
            login(request, user=user)
            return redirect(reverse('home:home'))
        else:
            messages.error(request, 'Invalid User')
            return redirect(reverse('home:login'))

    return render(
        request,
        'core/pages/login.html',
        context={
            'site_title': 'Login',
            'header_title': 'Login',
            'header_subtitle': 'Login into your account.',
        }
    )


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('home:login'))


def register_user(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user=user)
            messages.success(request, 'User created Succesfully.')
            return redirect(reverse('home:home'))
        else:
            messages.error(request, 'Error while trying to register')
            return redirect(reverse('home:register'))

    return render(
        request,
        'core/pages/register.html',
        context={
            'form': form,
            'site_title': 'Register',
            'header_title': 'Register',
            'header_subtitle': 'Create a new account.',
        }
    )
