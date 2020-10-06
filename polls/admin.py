from django.contrib import admin
from .models import Search, Ad


class AdFields(admin.ModelAdmin):
    list_display = ("title", "location", "status")
    readonly_fields = ("title", "location", "site", "description", "link")


class SearchFields(admin.ModelAdmin):
    list_display = ("web", "subject")
    list_filter = ('web',)


admin.site.register(Search, SearchFields)
admin.site.register(Ad, AdFields)

admin.site.site_header = "Pannel Admin Django"
