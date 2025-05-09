# main.py — CLI version using TextBlob-based AI logic

from dotenv import load_dotenv
import os
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth
from mood_parser import get_genres_for_input
from valid_genres import VALID_SPOTIFY_GENRES

# Load Spotify credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private",
    cache_path=".cache"
))

# Get user input
prompt = input("Describe your vibe: ").strip()
if not prompt:
    print("Please enter something.")
    exit()

# Analyze mood and genres
mood, genres = get_genres_for_input(prompt)
selected_genre = random.choice(genres) if genres else "pop"

print(f"Mood detected: {mood}")
print(f"Using genre: {selected_genre}")

# Search for tracks
try:
    results = sp.search(q=f"genre:{selected_genre}", type="track", limit=30)
    tracks = results["tracks"]["items"]
    uris = [t["uri"] for t in tracks]
except Exception as e:
    print("Spotify search failed:", e)
    exit()

if not uris:
    print("No tracks found.")
    exit()

# Create playlist
user = sp.current_user()
playlist = sp.user_playlist_create(
    user=user["id"],
    name=f"{mood.title()} Vibes",
    description=f"Generated from: {prompt}",
    public=True
)
sp.playlist_add_items(playlist["id"], uris)

print("Playlist created!")
print("Link:", playlist["external_urls"]["spotify"])