from django.db import models

from authentication.models import SteamUser


class Match(models.Model):
    match_id = models.BigIntegerField(unique=True)
    player = models.ForeignKey(SteamUser, on_delete=models.CASCADE, related_name='matches')
    hero_id = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    win = models.BooleanField()
    rating_change = models.IntegerField()
    match_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in seconds")
