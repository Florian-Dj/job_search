from django.db import models

web_choices = [('Linkedin', 'Linkedin'), ('Pole-Emploi', 'Pôle-Emploi')]
status_choice = [('not-read', 'Non Lu'), ('applied', 'Postulé'), ('inadequate', 'Inadéquate'),
                 ('expired', 'Expiré'), ('other', 'Autres')]


class Search(models.Model):
    objects = None
    web = models.CharField("Site", max_length=255, choices=web_choices)
    subject = models.CharField("Sujet", max_length=255, help_text="Nom du Post")
    link_search = models.CharField("Lien", max_length=255, unique=True)


class Ad(models.Model):
    objects = None
    site = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField("Titre", max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField("Localisation", max_length=255)
    link = models.CharField("Lien", max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=status_choice)


class Stat(models.Model):
    objects = None
    web = models.ForeignKey(Search, on_delete=models.CASCADE)
    not_read = models.IntegerField("Non lue", default=0)
    applied = models.IntegerField("Postulé", default=0)
    inadequate = models.IntegerField("Inadéquate", default=0)
    expired = models.IntegerField("Expiré", default=0)
    other = models.IntegerField("Autres", default=0)
    total = models.IntegerField("Total", default=0)
