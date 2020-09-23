from django.shortcuts import render
from .models import Search, Ad, Stat
from django.db.models import Sum, F


def index(request):
    all_stat = Stat.objects.order_by('web').annotate(
        p_notread=Sum(F('not_read') * 100 / F('total')),
        p_applied=Sum(F('applied') * 100 / F('total')),
        p_inadequate=Sum(F('inadequate') * 100 / F('total')),
        p_expired=Sum(F('expired') * 100 / F('total')),
        p_other=Sum(F('other') * 100 / F('total'))
    )
    total_stat = all_stat.aggregate(
        t_not_read=Sum('not_read'),
        t_applied=Sum('applied'),
        t_inadequate=Sum('inadequate'),
        t_expired=Sum('expired'),
        t_other=Sum('other'),
        t_total=Sum('total'),
        pt_not_read=Sum('not_read') * 100 / Sum('total'),
        pt_applied=Sum('applied') * 100 / Sum('total'),
        pt_inadequate=Sum('inadequate') * 100 / Sum('total'),
        pt_expired=Sum('expired') * 100 / Sum('total'),
        pt_other=Sum('other') * 100 / Sum('total'))
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
    status = request.GET.get('status', 'not-read')
    site = request.GET.get('site', '')
    if not site and not status:
        ad_list = Ad.objects.all()
    elif not status:
        ad_list = Ad.objects.filter(site__web=site)
    elif not site:
        ad_list = Ad.objects.filter(status=status)
    else:
        ad_list = Ad.objects.filter(status=status, site__web=site)
    context = {
        'ad_list': ad_list,
        'status': status,
        'site': site,
    }
    return render(request, 'ad.html', context)


def contact(request):
    return render(request, 'contact.html')
