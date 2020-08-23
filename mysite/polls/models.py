from django.db import models


class Search(models.Model):
    web = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    link_search = models.CharField(max_length=255)
    link_ad = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.web, self.subject)


class Ad(models.Model):
    site = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    link = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255)
