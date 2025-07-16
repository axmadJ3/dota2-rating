from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from authentication.models import SteamUser
from .models import Match
from .services import sync_matches_for_player
from .utils import hero_name
from .serializers import SteamUserSerializer


def rating_dashboard_view(request):
    user_total_rating = 0

    if request.user.is_authenticated:
        user_with_rating = (
            SteamUser.objects
            .annotate_total_rating()
            .get(pk=request.user.pk)
        )
        user_total_rating = round(user_with_rating.total_rating, 2)

        return render(request, 'index.html', {
            'user_total_rating': user_total_rating,
        })
    else:
        return render(request, 'index.html', )


@api_view(['GET'])
def leaderboard(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 50))

    users = SteamUser.objects.annotate_total_rating().order_by('-total_rating')[offset:offset + limit]
    return Response(SteamUserSerializer(users, many=True).data)


@api_view(['GET'])
def player_position(request):
    steam_id = request.GET.get('steam_id')
    if not steam_id:
        return Response({"error": "steam_id is required"}, status=400)

    all_users = SteamUser.objects.annotate_total_rating().order_by('-total_rating')

    try:
        user = all_users.get(steamid=steam_id)
        position = list(all_users).index(user) + 1
    except SteamUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    return Response({
        "position": position,
        "nickname": user.personaname,
        "rating": round(user.total_rating, 2)
    })


@api_view(['GET'])
def user_stats(request):
    steam_id = request.GET.get('steam_id')
    if not steam_id:
        return Response({"error": "steam_id is required"}, status=400)

    try:
        user = SteamUser.objects.get(steamid=steam_id)
    except SteamUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))

    matches = Match.objects.filter(player=user).order_by('-match_time')[offset:offset + limit]

    return Response([
        {
            "time": m.match_time,
            "duration": m.duration,
            "hero": hero_name(m.hero_id),
            "result": "Win" if m.win else "Lose",
            "kills": m.kills,
            "deaths": m.deaths,
            "assists": m.assists,
            "rating": m.rating_change,
        } for m in matches
    ])


@api_view(['POST'])
def sync_player_matches(request):
    steam_id = request.data.get('steam_id')
    if not steam_id:
        return Response({"error": "steam_id is required"}, status=400)

    try:
        user = SteamUser.objects.get(steamid=steam_id)
    except SteamUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    sync_matches_for_player(user)
    return Response({"status": "ok"})
