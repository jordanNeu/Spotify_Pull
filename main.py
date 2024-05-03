from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_ID = "40af1c79af3841689a8d380dd117df5e"
SPOTIFY_SECRET = "74a39da0fcd14c0eb90a07ab9fcc740c"
URL_REDIRECT = "https://example.com"

spotify = spotipy.oauth2.SpotifyOAuth(
    client_id = SPOTIFY_ID,
    client_secret= SPOTIFY_SECRET,
    redirect_uri=URL_REDIRECT,
    scope="playlist-modify-private",
    cache_path="token.txt")
access_token = spotify.get_access_token()

spotify_client = spotipy.Spotify(auth_manager=spotify)

user_id = spotify_client.current_user()["id"]
date = input("What year would you like to travel to? In YYYY-MM-DD format.")
# URL = f"https://www.billboard.com/charts/hot-100/{date}/"
#
# response = requests.get(URL)
# webpage = response.text
#
# soup = BeautifulSoup(webpage, "html.parser")
# titles = soup.find_all("h3", class_="u-max-width-330")
# artists = soup.select("ul li h3#title-of-a-story~span")

year = date.split("-")[0]
with open("top100.txt", "r") as file:
    song_titles = file.readlines()
titles = [title.strip() for title in song_titles]
song_uris = []
# for song in titles:
#     lists = song.getText().strip()
#     with open("top100.txt", "a") as file:
#         file.write(f"{lists}\n")

for song in titles:
    results = spotify_client.search(q=f"track:{song}", type="track", limit=50)
    uri = results["tracks"]["items"][0]["uri"]
    song_uris.append(uri)
    print(results["tracks"]["items"][0]["uri"])

playlist = spotify_client.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
spotify_client.playlist_add_items(playlist_id=playlist["id"], items=song_uris)