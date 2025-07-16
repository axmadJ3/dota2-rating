from django.core.management.base import BaseCommand

from authentication.models import SteamUser
from rating.services import sync_matches_for_player

class Command(BaseCommand):
    help = 'Syncs all matches and updates the rating of all players'

    def handle(self, *args, **options):
        total = 0
        for player in SteamUser.objects.exclude(steamid__isnull=True):
            self.stdout.write(f"Sync for {player.personaname} ({player.steamid})")
            sync_matches_for_player(player)
            total += 1
        self.stdout.write(self.style.SUCCESS(f"Sync players: {total}"))
