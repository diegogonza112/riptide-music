import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

SPOTIPY_CLIENT_ID = "648d2baba64542109c3b9eb8d9525798"
SPOTIPY_CLIENT_SECRET = "31858e4f138a414aa1874fe5488f76e7"
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/"
SCOPE = "user-top-read"


def read():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=
                                                   SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=
                                                   SPOTIPY_REDIRECT_URI,
                                                   scope=SCOPE))
    results = sp.current_user_top_tracks()

    return results


print(read())
