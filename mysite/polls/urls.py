from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recherches', views.search, name='recherche'),
    path('annonces', views.ad, name='annonces')
]