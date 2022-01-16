import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

SPOTIPY_CLIENT_ID = "ca227eab01e349dfac9691f88f7c9d80"
SPOTIPY_CLIENT_SECRET = "119a23b3da1a4fcf82cf8c9e2936a677"
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
