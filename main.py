from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

date = input('Which year do you want to travel to? Type the date in format YYYY-MM-DD: ')
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

responce = requests.get(URL)

soup = BeautifulSoup(responce.text, 'html.parser')
all_songs_h3 = soup.find_all('h3', id='title-of-a-story', class_='a-no-trucate')
song_names = [song.getText().strip() for song in all_songs_h3]
authors_tag = soup.find_all(name='span', class_='a-no-trucate')
authors = [author.getText().strip() for author in authors_tag]
#print(song_names)
#print(authors)


OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://example.com',
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        show_dialog=True,
        cache_path='token.txt'
    )
)
user_id = sp.current_user()['id']
print(user_id)

#date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
#song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)