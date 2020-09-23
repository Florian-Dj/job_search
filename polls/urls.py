from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('recherche', views.search, name='recherche'),
    path('annonce', views.ad, name='annonce'),
    path('contact', views.contact, name='contact')
]