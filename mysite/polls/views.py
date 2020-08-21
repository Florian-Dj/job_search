from django.shortcuts import render
from .models import Search
from django.http import HttpResponse


def index(request):
    context = {
        "name": "Mucral"
    }
    return render(request, 'home.html', context)
# Create your views here.


def search(request):
    search_list = Search.objects.all()
    context = {
        'search_list': search_list
    }
    return render(request, 'search.html', context)


def ad(request):
    return render(request, 'ad.html')
