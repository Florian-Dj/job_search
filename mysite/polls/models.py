from django.db import models


class Search(models.Model):
    web_choices = [('Leboncoin', 'Leboncoin'), ('Linkedin', 'Linkedin'), ('Pôle-Emploi', 'Pôle-Emploi')]
    web = models.CharField(max_length=255, choices=web_choices)
    subject = models.CharField(max_length=255)
    link_search = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{} - {}".format(self.web, self.subject)


class Ad(models.Model):
    site = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    location = models.CharField(max_length=255)
    link = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return "{} / {}".format(self.title, self.location)


