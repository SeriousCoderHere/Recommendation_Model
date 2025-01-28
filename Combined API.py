# MAL API
mport mysql.connector as c
import requests

# Function to establish a connection to the MySQL database
def create_connection():
    return c.connect(host="localhost", user="root", password="1234", database="Prod_Reccomend_Sys")

# Function to store recommendations in the ML_RECCOMENDATION table
def store_recommendations(recommendations, user_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        for rec in recommendations:
            content_id = rec['mal_id']  # Assuming 'mal_id' is the ID used in Content_Store
            title = rec['title']
            score = rec.get('score', 0)  # Default score to 0 if not available
            description = rec.get('synopsis', '')  # Default to empty if not available
            
            # Insert into ML_RECCOMENDATION table
            cursor.execute('''
            INSERT INTO ML_RECCOMENDATION (uID, ContentID, Score, Description)
            VALUES (%s, %s, %s, %s)
            ''', (user_id, content_id, score, description))
        
        connection.commit()
        print("Recommendations stored successfully.")
    
    except c.Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main function to execute the workflow
def main(anime_id, user_id):
    # Fetch anime recommendations
    data = fetch_anime_data(anime_id)
    
    if data and 'data' in data:
        recommendations = data['data']
        store_recommendations(recommendations, user_id)
    else:
        print("No recommendations found.")

# OpenLibrary API

import requests
import mysql.connector as c

def create_connection():
    """Establish a connection to the MySQL database."""
    return c.connect(host="localhost", user="root", password="1234", database="Prod_Reccomend_Sys")

def insert_book_to_db(book):
    """Insert book data into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO Content_Store (title, author, year, genre, description, url, imglink)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (book['title'], book['author'], book['year'], book['genre'], book['description'], book['url'], book['imglink']))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_books_from_openlibrary(genre, description, max_results=5):
    """Fetch books from OpenLibrary based on genre and description."""
    query = f"{genre} {description}".strip()
    url = f"https://openlibrary.org/search.json?q={query}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        books = data.get('docs', [])
        
        for book in books[:max_results]:
            languages = book.get('language', [])
            if 'eng' in languages:
                title = book.get('title', "Unknown Title")
                author = ', '.join(book.get('author_name', ["Unknown Author"]))
                year = book.get('first_publish_year', 'Unknown')
                book_url = f"https://openlibrary.org{book.get('key', '')}" if book.get('key') else "URL not available"
                cover_id = book.get('cover_i', None)
                imglink = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "Cover image not available"

                book_data = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "description": description,
                    "url": book_url,
                    "imglink": imglink
                }
                
                # Insert book data into the database
                insert_book_to_db(book_data)

    else:
        print("Failed to fetch books from OpenLibrary.")

#Spotify API

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
