from django.contrib import admin
from .models import Search, Ad, Stat, Mail


class AdFields(admin.ModelAdmin):
    list_display = ("title", "location", "status")
    readonly_fields = ("title", "location", "site", "description", "link")
    list_filter = ("site__web", "site__subject", "status",)


class SearchFields(admin.ModelAdmin):
    list_display = ("web", "subject")
    list_filter = ('web',)


class StatFields(admin.ModelAdmin):
    list_display = ("web", "not_read", "applied", "inadequate", "expired", "other", "total")
    readonly_fields = ("web", "not_read", "applied", "inadequate", "expired", "other", "total")


class MailFields(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "message")


admin.site.register(Search, SearchFields)
admin.site.register(Ad, AdFields)
admin.site.register(Stat, StatFields)
admin.site.register(Mail, MailFields)

admin.site.site_header = "Pannel Admin Django"
