from django.core.management.base import BaseCommand

from authentication.models import SteamUser
from rating.services import sync_matches_for_player

class Command(BaseCommand):
    help = 'Синхронизирует все матчи и обновляет рейтинг всех игроков'

    def handle(self, *args, **options):
        total = 0
        for player in SteamUser.objects.exclude(steamid__isnull=True):
            self.stdout.write(f"⏳ Синхронизация для {player.personaname} ({player.steamid})")
            sync_matches_for_player(player)
            total += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Синхронизировано игроков: {total}"))
