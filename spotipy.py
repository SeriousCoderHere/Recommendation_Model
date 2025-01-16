import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_id='872ce50d85c34064af5e0897c9342ff3'
client_secret='44f8f49bf3de420caa117723bcc52f3c'
client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def fetch_categories(limit=10):
    categories = sp.categories(limit=limit)['categories']['items']
    return {category['name'] for category in categories}

def fetch_playlists(category_id, limit=10):
    playlists = sp.category_playlists(category_id=category_id, limit=limit)['playlists']['items']
    return [{"name": playlist['name'], "id": playlist['id']} for playlist in playlists]

def fetch_tracks(category_id, limit=5, max_tracks=10):
    playlists = sp.category_playlists(category_id=category_id, limit=limit)['playlists']['items']

    all_tracks = []

    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        
        tracks = sp.playlist_tracks(playlist_id, limit=max_tracks)['items']
        
        for track in tracks:
            track_info = track['track']
            all_tracks.append({
                "track_name": track_info['name'],
                "artist": ', '.join([artist['name'] for artist in track_info['artists']]),
                "album": track_info['album']['name'],
                "playlist_name": playlist_name,
                "spotify_url": track_info['external_urls']['spotify']
            })    
    return all_tracks

c=fetch_categories()
category=str(input(f"what category do you like?\n{c}: "))
input=int(input('how would you like your recommended results? \ntracks(1) \n playlists(2) \n both(3)\n'))

if input == 2:
    results=fetch_playlists(category)
elif input == 1:
    results=fetch_tracks(category_id)
print(results)
