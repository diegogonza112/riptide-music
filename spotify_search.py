import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "648d2baba64542109c3b9eb8d9525798"
SPOTIPY_CLIENT_SECRET = "31858e4f138a414aa1874fe5488f76e7"
SPOTIPY_REDIRECT_URI = "https://hidden-castle-24851.herokuapp.com/login"
SCOPE = "user-read-email, user-read-currently-playing, user-read-playback-state"


def new_rel():
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=
                                                SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=
                                                SPOTIPY_REDIRECT_URI,
                                                scope=SCOPE
                                                ))

    data = sp.new_releases(limit=5)
    info = []
    for i in data['albums']['items']:
        y = i['name']
        l = i['album_type']
        for j in i['artists']:
            x = j['name']
            info.append(l.title() + ': ' + y + ' by ' + x)
            break

    return info


class SpotifySearch:

    def __init__(self, song):
        self.song = song

    def song_info(self):
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                    client_secret=
                                                    SPOTIPY_CLIENT_SECRET,
                                                    redirect_uri=
                                                    SPOTIPY_REDIRECT_URI,
                                                    scope=SCOPE
                                                    ))

        data = sp.search(q=self.song, type="track", limit=15)
        info = []
        for i in data["tracks"]["items"]:
            x = {"Song Name": i['name'], "Artist(s)": i['artists'][0]['name'],
                 "Album": i["album"]['name'],
                 "Year": i["album"]["release_date"]}
            for j in range(len(i["album"]["images"])):
                if i["album"]["images"][j]["url"]:
                    x["Album Art"] = i["album"]["images"][j]["url"]
                    break
            for j in range(len(i['artists'])):
                if i['artists'][j]['name']:
                    x["Artist(s)"] = i['artists'][j]['name']
                    break
            if "Artist(s)" not in x:
                x["Artist(s)"] = "N/A"
            if "Album Art" not in x:
                x["Album Art"] = 'https://i.scdn.co/image/ab67616d0000b273cad19' \
                                 '0f1a73c024e5a40dddd'

            info.append(x)
        return info


ss = SpotifySearch("yes")
print(new_rel())
