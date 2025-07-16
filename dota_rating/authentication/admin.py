from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import SteamUser

@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    list_display = ['personaname', 'steamid', 'total_rating_display']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_rating=Coalesce(Sum('matches__rating_change'), 0)
        )

    @admin.display(ordering='total_rating', description='Rating')
    def total_rating_display(self, obj):
        return round(obj.total_rating, 2)
