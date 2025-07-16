import requests
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Match
from .utils import calculate_rating_change

def sync_matches_for_player(player):
    url = f"https://api.opendota.com/api/players/{player.steamid}/matches?game_mode=23&significant=0"
    response = requests.get(url)
    if not response.ok:
        return

    matches = response.json()
    cutoff_date = timezone.now() - timedelta(days=180)

    Match.objects.filter(player=player, match_time__lt=cutoff_date).delete()

    for m in matches:
        match_time = datetime.fromtimestamp(m['start_time'], tz=timezone.utc)

        if match_time < cutoff_date:
            continue

        if Match.objects.filter(match_id=m['match_id']).exists():
            continue

        win = (m['player_slot'] < 128 and m['radiant_win']) or (m['player_slot'] >= 128 and not m['radiant_win'])
        rating_change = calculate_rating_change(win, m['kills'], m['deaths'], m['assists'])

        Match.objects.create(
            match_id=m['match_id'],
            player=player,
            hero_id=m['hero_id'],
            kills=m['kills'],
            deaths=m['deaths'],
            assists=m['assists'],
            win=win,
            rating_change=rating_change,
            match_time=match_time,
            duration=m['duration'],
        )
