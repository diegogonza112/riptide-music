import json

import requests
import spotipy.util
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64

SPOTIPY_CLIENT_ID = "648d2baba64542109c3b9eb8d9525798"
SPOTIPY_CLIENT_SECRET = "31858e4f138a414aa1874fe5488f76e7"
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/login"
SCOPE = "user-read-email, user-read-currently-playing, user-read-playback-state"


class SpotifyAuth:

    def __init__(self):
        self.unused = True
        self.success = False
        self.username = ''

    def user(self):
        if self.unused:
            sp = spotipy.Spotify(
                client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                        client_secret=
                                                        SPOTIPY_CLIENT_SECRET,
                                                        redirect_uri=
                                                        SPOTIPY_REDIRECT_URI,
                                                        scope=SCOPE
                                                        ))
            return sp.me()['display_name']
        else:
            return self.username

sa = SpotifyAuth()
print(sa.user())
