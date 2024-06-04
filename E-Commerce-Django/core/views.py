from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request,
        'core/pages/home.html',
        context={'site_title': 'Test'}
    )
