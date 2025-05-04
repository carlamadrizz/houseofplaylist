# main.py — CLI version for AI Playlist Generator (genre-based only)

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mood_parser import detect_mood_from_prompt, mood_to_features
from valid_genres import VALID_SPOTIFY_GENRES

# Load .env credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private user-library-read",
    open_browser=True,
    cache_path=".cache",
    show_dialog=True
))

# Identify user
user = sp.current_user()
user_id = user["id"]
print(f"👤 Logged in as: {user['display_name']} ({user_id})")

# Genre mapping based on mood
def mood_to_genres(mood):
    genre_map = {
        "happy": ["pop", "dance"],
        "sad": ["acoustic", "piano"],
        "chill": ["ambient", "study"],
        "hype": ["hip-hop", "edm"],
        "angry": ["metal", "punk"],
        "romantic": ["r-n-b", "soul"]
    }
    return [g for g in genre_map.get(mood, ["pop"]) if g in VALID_SPOTIFY_GENRES][:1]

# Get user input
prompt = input("What's the vibe? > ").strip()
if not prompt:
    print("❌ No vibe entered.")
    exit()

# Detect mood and map genre
mood = detect_mood_from_prompt(prompt)
genres = mood_to_genres(mood)

print(f"🎯 Mood: {mood}")
print(f"🔍 Searching for tracks in genre: {genres[0]}")

# Perform search query
try:
    results = sp.search(q=f"genre:{genres[0]}", type="track", limit=30)
    tracks = results["tracks"]["items"]
    track_uris = [track["uri"] for track in tracks]
except Exception as e:
    print(f"❌ Spotify search failed: {e}")
    exit()

if not track_uris:
    print("⚠️ No tracks found.")
    exit()

# Create playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"House of Playlist - {mood.title()} Vibes",
    public=True,
    description=f"Generated from: {prompt}"
)
sp.playlist_add_items(playlist["id"], track_uris)

print("✅ Playlist created!")
print("🎧 Link:", playlist["external_urls"]["spotify"])