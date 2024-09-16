from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    """
    Retrieve the Spotify tokens for a given session ID.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        SpotifyToken: The SpotifyToken object for the user, or None if not found.
    """
    user_tokens = SpotifyToken.objects.filter(user=session_id)

    if user_tokens.exists():
        return user_tokens[0]
    return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    """
    Update existing tokens or create new tokens for a given session ID.

    Args:
        session_id (str): The session ID of the user.
        access_token (str): The new access token.
        token_type (str): The type of the token.
        expires_in (int): The number of seconds until the token expires.
        refresh_token (str): The refresh token.
    """
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in
        )
        tokens.save()


def is_spotify_authenticated(session_id):
    """
    Check if the Spotify tokens for a given session ID are still valid.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        bool: True if the tokens are valid, False otherwise.
    """
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False


def refresh_spotify_token(session_id):
    """
    Refresh the Spotify tokens for a given session ID using the refresh token.

    Args:
        session_id (str): The session ID of the user.
    """
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    """
    Execute a Spotify API request for a given session ID and endpoint.

    Args:
        session_id (str): The session ID of the user.
        endpoint (str): The Spotify API endpoint to call.
        post_ (bool): Whether to use a POST request.
        put_ (bool): Whether to use a PUT request.

    Returns:
        dict: The JSON response from the Spotify API, or an error message.
    """
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {tokens.access_token}"
    }

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except Exception:
        return {'Error': 'Issue with request'}


def play_song(session_id):
    """
    Send a request to the Spotify API to play a song for a given session ID.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        dict: The JSON response from the Spotify API.
    """
    return execute_spotify_api_request(session_id, "player/play", put_=True)


def pause_song(session_id):
    """
    Send a request to the Spotify API to pause a song for a given session ID.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        dict: The JSON response from the Spotify API.
    """
    return execute_spotify_api_request(session_id, "player/pause", put_=True)


def skip_song(session_id):
    """
    Send a request to the Spotify API to skip a song for a given session ID.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        dict: The JSON response from the Spotify API.
    """
    return execute_spotify_api_request(session_id, "player/next", post_=True)