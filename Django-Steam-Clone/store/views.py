from django.shortcuts import render
from django.views.generic import View


class StorePage(View):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            'store/pages/store.html',
            {'title': 'Store'}
        )
