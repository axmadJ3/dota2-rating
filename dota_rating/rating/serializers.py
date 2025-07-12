from rest_framework import serializers

from authentication.models import SteamUser


class SteamUserSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='total_rating')

    class Meta:
        model = SteamUser
        fields = ['steamid', 'personaname', 'rating']
