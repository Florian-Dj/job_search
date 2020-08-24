from django.db import models


class Search(models.Model):
    web_choices = [('Leboncoin', 'Leboncoin'), ('Linkedin', 'Linkedin'), ('Pole-Emploi', 'Pôle-Emploi')]
    web = models.CharField("Site", max_length=255, choices=web_choices)
    subject = models.CharField("Sujet", max_length=255)
    link_search = models.CharField("Lien", max_length=255, unique=True)

    def __str__(self):
        return "{} - {}".format(self.web, self.subject)


class Ad(models.Model):
    status_choice = [('not-read', 'Non Lu'), ('applied', 'Postulé'), ('inadequate', 'Inadéquate'), ('expired', 'Expiré')]
    site = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField("Titre", max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField("Localisation", max_length=255)
    link = models.CharField("Lien", max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=status_choice)

    def __str__(self):
        return "{} / {}".format(self.title, self.location)
