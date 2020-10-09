from django.shortcuts import render
from .models import Search, Ad, Stat
from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from .forms import ContactForm


def index(request):
    all_stat_search = Stat.objects.order_by("web").annotate(
        p_notread=Sum(F('not_read') * 100 / F('total')),
        p_applied=Sum(F('applied') * 100 / F('total')),
        p_inadequate=Sum(F('inadequate') * 100 / F('total')),
        p_expired=Sum(F('expired') * 100 / F('total')),
        p_other=Sum(F('other') * 100 / F('total'))
    )

    total_stat = all_stat_search.aggregate(
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

    all_stat_site = Stat.objects.values('web__web').annotate(
        Sum('not_read'),
        Sum('applied'),
        Sum('inadequate'),
        Sum('expired'),
        Sum('other'),
        Sum('total'),
        pt_not_read=Sum('not_read') * 100 / Sum('total'),
        pt_applied=Sum('applied') * 100 / Sum('total'),
        pt_inadequate=Sum('inadequate') * 100 / Sum('total'),
        pt_expired=Sum('expired') * 100 / Sum('total'),
        pt_other=Sum('other') * 100 / Sum('total')
    )

    context = {
        'all_stat_search': all_stat_search,
        'all_stat_site': all_stat_site,
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            auth_user = form.cleaned_data['name']
            from_email = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = "{} <{}>".format(auth_user, from_email)

            recipients = ['floriandjerbi@gmail.com']

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
