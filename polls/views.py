from django.shortcuts import render
from .models import Search, Ad, Stat
from . import scrape
from django.db.models import Sum


def index(request):
    all_stat = Stat.objects.all()
    total_stat = all_stat.aggregate(Sum('not_read'), Sum('applied'), Sum('inadequate'), Sum('expired'), Sum('other'), Sum('total'))
    context = {
        'all_stat': all_stat,
        'total_stat': total_stat,
    }
    return render(request, 'home.html', context)


def search(request):
    search_list = Search.objects.order_by('web')
    context = {
        'search_list': search_list
    }
    return render(request, 'search.html', context)


def ad(request):
    if request.GET.get('ads', '') == "search":
        scrape.home()
    status = request.GET.get('status', 'not-read')
    site = request.GET.get('site', '')
    if not site and not status:
        ad_list = Ad.objects.all()
    elif not status:
        ad_list = Ad.objects.filter(site__subject=site)
    elif not site:
        ad_list = Ad.objects.filter(status=status)
    else:
        ad_list = Ad.objects.filter(status=status, site__subject=site)
    context = {
        'ad_list': ad_list,
        'status': status,
        'site': site,
    }
    return render(request, 'ad.html', context)
