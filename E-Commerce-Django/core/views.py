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
