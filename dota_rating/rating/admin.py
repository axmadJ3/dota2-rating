from django.contrib import admin

from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'player')
