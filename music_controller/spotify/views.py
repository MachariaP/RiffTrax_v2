from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens, is_spotify_authenticated, execute_spotify_api_request, pause_song, play_song, skip_song
from api.models import Room
from .models import Vote


class AuthURL(APIView):
    """
    API view to generate the Spotify authorization URL.
    """
    def get(self, request, format=None):
        """
        Handle GET request to generate the Spotify authorization URL.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response containing the authorization URL.
        """
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    """
    Handle the Spotify callback after user authorization.

    Args:
        request (HttpRequest): The request object.
        format (str, optional): The format of the response.

    Returns:
        HttpResponseRedirect: A redirect to the frontend.
    """
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    """
    API view to check if the user is authenticated with Spotify.
    """
    def get(self, request, format=None):
        """
        Handle GET request to check if the user is authenticated with Spotify.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response containing the authentication status.
        """
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class CurrentSong(APIView):
    """
    API view to get the currently playing song in the room.
    """
    def get(self, request, format=None):
        """
        Handle GET request to get the currently playing song in the room.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response containing the current song information.
        """
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name

        votes = len(Vote.objects.filter(room=room, song_id=song_id))
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }

        self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        """
        Update the current song in the room.

        Args:
            room (Room): The room object.
            song_id (str): The ID of the current song.
        """
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])
            votes = Vote.objects.filter(room=room).delete()


class PauseSong(APIView):
    """
    API view to pause the currently playing song.
    """
    def put(self, request, format=None):
        """
        Handle PUT request to pause the currently playing song.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response indicating the result of the operation.
        """
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_403_FORBIDDEN)


class PlaySong(APIView):
    """
    API view to play the currently paused song.
    """
    def put(self, request, format=None):
        """
        Handle PUT request to play the currently paused song.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response indicating the result of the operation.
        """
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response({}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    """
    API view to skip the currently playing song.
    """
    def post(self, request, format=None):
        """
        Handle POST request to skip the currently playing song.

        Args:
            request (HttpRequest): The request object.
            format (str, optional): The format of the response.

        Returns:
            Response: A response indicating the result of the operation.
        """
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            vote = Vote(user=self.request.session.session_key,
                        room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)