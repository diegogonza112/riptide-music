import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

SPOTIPY_CLIENT_ID = "648d2baba64542109c3b9eb8d9525798"
SPOTIPY_CLIENT_SECRET = "31858e4f138a414aa1874fe5488f76e7"
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/"
SCOPE = "user-top-read"
TOKEN = "BQCBv5qY6xax0kNy28mqACbwqmQulDNdqoPWse4MnqagXgBimLyC0rn0zvgwbUEomwz" \
        "PTi-6n2N9nY8vpLKpmYc_jTufuNrlkPWWDcCc_Jw82MWPcKPC0Q3AKJJLsbx6gHhPtBDE" \
        "re2pl8o"


def user():
    sp = spotipy.Spotify(TOKEN,
                         auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=
                                                   SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=
                                                   SPOTIPY_REDIRECT_URI,
                                                   scope=SCOPE
                                                   ))
    return sp.me()['display_name']
