import requests
from django.core.management.base import BaseCommand
from authentication.models import SteamUser
from django.utils import timezone

class Command(BaseCommand):
    help = 'Downloads test players from the OpenDota API who have Turbo matches.'

    def handle(self, *args, **options):
        self.stdout.write("Uploading public profiles...")
        r = requests.get("https://api.opendota.com/api/proPlayers")
        if not r.ok:
            self.stdout.write(self.style.ERROR("Couldn't get a list of pro players"))
            return

        players = r.json()
        created = 0

        for player in players:
            account_id = player.get("account_id")
            if not account_id:
                continue

            matches_url = f"https://api.opendota.com/api/players/{account_id}/matches?game_mode=23&significant=0&limit=1"
            matches_resp = requests.get(matches_url)
            if not matches_resp.ok or not matches_resp.json():
                continue

            profile_url = f"https://api.opendota.com/api/players/{account_id}"
            profile_resp = requests.get(profile_url)
            if not profile_resp.ok:
                continue

            profile = profile_resp.json().get("profile")
            if not profile:
                continue

            steamid = str(profile.get("steamid", account_id))
            if SteamUser.objects.filter(steamid=steamid).exists():
                continue

            SteamUser.objects.create_user(
                steamid=steamid,
                password=None,
                personaname=profile.get("personaname", ""),
                profileurl=profile.get("profileurl", ""),
                avatar=profile.get("avatar", ""),
                avatarmedium=profile.get("avatarmedium", ""),
                avatarfull=profile.get("avatarfull", ""),
                is_active=True,
                date_joined=timezone.now(),
            )

            created += 1
            self.stdout.write(f"Added: {profile.get('personaname', steamid)}")

            if created >= 60:
                break

        self.stdout.write(self.style.SUCCESS(f"\nTotal players added: {created}"))
