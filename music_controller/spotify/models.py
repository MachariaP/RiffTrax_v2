from django.db import models
from api.models import Room

class SpotifyToken(models.Model):
    """
    This model represents a Spotify token. It contains the user's unique identifier, 
    the creation time of the token, the refresh token, the access token, 
    the expiration time of the token, and the token type.
    """
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Vote(models.Model):
    """
    This model represents a vote. It contains the user's unique identifier, 
    the creation time of the vote, the song id that the vote is for, 
    and a foreign key to the room where the vote was made.
    """
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)