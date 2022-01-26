import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyOAuth
import config

SPOTIPY_CLIENT_ID = config.user
SPOTIPY_CLIENT_SECRET = config.secret
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/login"
SCOPE = "user-read-email, user-read-currently-playing, user-read-playback-state"


class SpotifyAuth:

    def __init__(self):
        self.unused = True
        self.success = False
        self.username = ''
        self._userID = ''

    def user(self, user):
        if self.unused:
            sp = spotipy.Spotify(
                client_credentials_manager=SpotifyOAuth(
                    client_id=SPOTIPY_CLIENT_ID,
                    client_secret=
                    SPOTIPY_CLIENT_SECRET,
                    redirect_uri=
                    SPOTIPY_REDIRECT_URI,
                    scope=SCOPE
                    ))
            if sp.user(user)['display_name'] != config.guest:
                self.username = sp.user(user)['display_name']

            self._userID = sp.user(user)['display_name']
            self.success = True
            self.unused = False

