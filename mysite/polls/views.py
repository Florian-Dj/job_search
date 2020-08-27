from django.shortcuts import render
from .models import Search, Ad
from . import run
from django.db.models import Count


def index(request):
    all_ad = Ad.objects.all()
    all_status = all_ad.values('status').annotate(dcount=Count('status'))
    all_site = all_ad.values('site__web').annotate(dcount=Count('site__web'))
    all_pe = all_ad.values('status').annotate(dcount=Count('status')).filter(site__web='Pole-Emploi')
    all_lb = all_ad.values('status').annotate(dcount=Count('status')).filter(site__web='Leboncoin')
    all_lk = all_ad.values('status').annotate(dcount=Count('status')).filter(site__web='Linkedin')
    if request.GET.get('mybtn', ''):
        run.home()
    context = {
        'all_ad': all_ad,
        'all_status': all_status,
        'all_site': all_site,
        'all_pe': all_pe,
        'all_lb': all_lb,
        'all_lk': all_lk
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
    site = request.GET.get('site', '')
    if not site and not select:
        ad_list = Ad.objects.all()
    elif not select:
        ad_list = Ad.objects.filter(site__web=site)
    elif not site:
        ad_list = Ad.objects.filter(status=select)
    else:
        ad_list = Ad.objects.filter(status=select, site__web=site)
    context = {
        'ad_list': ad_list,
        'status': select,
        'site': site,
    }
    return render(request, 'ad.html', context)
