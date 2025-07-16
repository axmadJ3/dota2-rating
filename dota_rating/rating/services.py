import requests
from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone
from .models import Match
from .utils import calculate_rating_change

def sync_matches_for_player(player):
    url = f"https://api.opendota.com/api/players/{player.steamid32}/matches?game_mode=23&significant=0"
    response = requests.get(url)
    if not response.ok:
        return

    matches = response.json()
    cutoff_date = timezone.now() - timedelta(days=180)

    old_matches = Match.objects.filter(player=player, match_time__lt=cutoff_date)
    for match in old_matches:
        print(f"Delete Match: {match.match_id}, Date: {match.match_time}")

    old_matches.delete()

    for m in matches:
        match_time = datetime.fromtimestamp(m['start_time'], tz=dt_timezone.utc)

        if match_time < cutoff_date:
            continue
        
        win = (m['player_slot'] < 128 and m['radiant_win']) or (m['player_slot'] >= 128 and not m['radiant_win'])
        rating_change = calculate_rating_change(win, m['kills'], m['deaths'], m['assists'])
        if Match.objects.filter(match_id=m['match_id']).exists():
            continue

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
        print("Add Match:", m['match_id'], "Rating:", rating_change)
