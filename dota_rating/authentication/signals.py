from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from rating.services import sync_matches_for_player

@receiver(user_logged_in)
def sync_on_login(sender, user, request, **kwargs):
    sync_matches_for_player(user)
