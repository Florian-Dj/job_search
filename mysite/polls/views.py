from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'home.html')
# Create your views here.


def search(request):
    return HttpResponse("Toutes les recherches ici même !")


def ad(request):
    return  HttpResponse("Toutes les annonces sont ici")
