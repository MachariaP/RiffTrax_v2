from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, CurrentSong, PauseSong, PlaySong, SkipSong

urlpatterns = [
    path('get-auth-url', AuthURL.as_view(), name='get-auth-url'),
    path('redirect', spotify_callback, name='spotify-callback'),
    path('is-authenticated', IsAuthenticated.as_view(), name='is-authenticated'),
    path('current-song', CurrentSong.as_view(), name='current-song'),
    path('pause', PauseSong.as_view(), name='pause-song'),
    path('play', PlaySong.as_view(), name='play-song'),
    path('skip', SkipSong.as_view(), name='skip-song'),
]