from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        "name":"Mucral"
    }
    return render(request, 'home.html', context)
# Create your views here.


def search(request):
    return render(request, 'search.html')


def ad(request):
    return render(request, 'ad.html')
