from django.contrib import admin

from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('player__personaname', 'match_id', 'match_time', 'rating_change', 'win')
    list_filter = ('win',)
    search_fields = ('player__personaname', 'match_id')
    ordering = ('-match_time',)
