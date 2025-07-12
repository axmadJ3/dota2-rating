from django.urls import path
from . import views


app_name = "api"

urlpatterns = [
    path('leaderboard', views.leaderboard),
    path('player-position', views.player_position),
    path('user/stats', views.user_stats),
    path('player/sync', views.sync_player_matches),
]
