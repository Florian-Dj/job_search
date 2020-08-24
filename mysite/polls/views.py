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
    select = request.GET.get('status', '')
    site = request.GET.get('site', '')
    if not site and not select:
        print("Here 1")
        ad_list = Ad.objects.all()
    elif not select:
        print("Here 2")
        ad_list = Ad.objects.filter(site__web=site)
    elif not site:
        print("Here 3")
        ad_list = Ad.objects.filter(status=select)
    else:
        print("Here 4")
        ad_list = Ad.objects.filter(status=select, site__web=site)
    context = {
        'ad_list': ad_list,
        'status': select,
        'site': site,
    }
    return render(request, 'ad.html', context)
