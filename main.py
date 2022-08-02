import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input("What year you would like to travel to? (YYYY-MM-DD) ")

#scraper
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", "html.parser")
response.raise_for_status()
soup = BeautifulSoup(response.text, features="html.parser")

title_list = []
headings = soup.select("h3.a-no-trucate")
for item in headings:
    title = item.get_text(strip=True)
    title_list.append(title)
print(title_list)

artist_list = []
spans = soup.select("span.a-no-trucate")
for item in spans:
    artist = item.get_text(strip=True)
    artist_list.append(artist)
print(artist_list)


#spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private, playlist-modify",
                                               client_id="",
                                               client_secret="",
                                               redirect_uri="http://localhost:1234",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               )
                     )
user_id = sp.current_user()["id"]

uri_list = []
for title in title_list:
    result = sp.search(q=f"track:{title}",type="track", limit=1)
    uri = result["tracks"]["items"][0]["uri"]
    split = uri.split(":", 3)
    uri_list.append(split[2])
print(uri_list)

sp.user_playlist_create(user=user_id, name=f"{date}")

playlists = sp.user_playlists(user=user_id)
for dicts in playlists["items"]:
    if dicts["name"] == date:
        playlist_id = dicts["id"]
print(playlist_id)

sp.playlist_add_items(playlist_id=playlist_id, items=uri_list)