from django.shortcuts import render
from .models import Search, Ad


def index(request):
    last_ad = Ad.objects.all().order_by("-id")[:10]
    last_ad = reversed(last_ad)
    context = {
        'last_ad': last_ad
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
    ad_list = Ad.objects.all()
    context = {
        'ad_list': ad_list
    }
    return render(request, 'ad.html', context)
