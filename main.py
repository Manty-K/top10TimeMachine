import requests
import keys
from bs4 import BeautifulSoup
import spotipy

# get date from User
date = input("Which year would you like to travel to? Type in this format YYYY-MM-DD\n")

# Extract Data form Billiboard
song_list = []
billi_url = f'https://www.billboard.com/charts/hot-100/{date}'
billi_response = requests.get(billi_url)

billi_data = billi_response.text

soup = BeautifulSoup(billi_data, 'html.parser')

tag_list = soup.findAll(class_='chart-element__information__song text--truncate color--primary')
print('Song List Created')

for tag in tag_list:
    song_list.append(tag.text)

# Search Songs and Extract URIs

uri_list = []

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=keys.spotify_client_id,client_secret=keys.spotify_client_secret,scope=scope,redirect_uri=keys.spotify_redirect_uri))

user_id = sp.current_user()['id']

for i in range(10):
    search_string = song_list[i]

    test = sp.search(q=search_string,type='track')
    name = test['tracks']['items'][0]['name']
    uri = test['tracks']['items'][0]['uri']
    uri_list.append(uri)
    print(f'Song \'{name}\' added')

print('All Songs added')

# Creating Playlist
cp_scope = 'playlist-modify-private'
cp_sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=keys.spotify_client_id,client_secret=keys.spotify_client_secret,scope=cp_scope,redirect_uri=keys.spotify_redirect_uri))

req = cp_sp.user_playlist_create(user=user_id,name=f'Billiboard Top 10 - {date}',public=False,description=f'Trending Songs on {date}')
playlist_id = req['id']

separator = ', '
uri_q = separator.join(uri_list)

add_items = cp_sp.playlist_add_items(playlist_id=playlist_id,items=uri_list)



