from django.shortcuts import render
from .models import Search, Ad
from . import run


def index(request):
    last_ad = Ad.objects.all().order_by("-id")[:10]
    if request.GET.get('mybtn', ''):
        run.home()
    context = {
        'last_ad': last_ad
    }
    return render(request, 'home.html', context)


def search(request):
    search_list = Search.objects.order_by('web')
    context = {
        'search_list': search_list
    }
    return render(request, 'search.html', context)


def ad(request):
    select = request.GET.get('status', 'not-read')
    status = ["not-red", "applied", "inadequate", "expired"]
    if select in status:
        ad_list = Ad.objects.filter(status=select)
    else:
        ad_list = Ad.objects.all()
    context = {
        'ad_list': ad_list,
        'status': select
    }
    return render(request, 'ad.html', context)
