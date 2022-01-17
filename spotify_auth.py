import json

import requests
import spotipy.util
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64

SPOTIPY_CLIENT_ID = "648d2baba64542109c3b9eb8d9525798"
SPOTIPY_CLIENT_SECRET = "31858e4f138a414aa1874fe5488f76e7"
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/login"
SCOPE = "user-read-email"


def user():
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=
                                                SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=
                                                SPOTIPY_REDIRECT_URI,
                                                scope=SCOPE
                                                ))
    return sp.me()['display_name']

print(user())
