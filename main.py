# main.py

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mood_parser import detect_mood_from_prompt, mood_to_features

# Load client credentials from .env
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private user-library-read",
    open_browser=True,
    cache_path=".cache",
    show_dialog=True
))

# Get user profile
user = sp.current_user()
user_id = user["id"]
print(f"👤 Logged in as: {user['display_name']} ({user_id})")

# Helper: Map mood to Spotify seed genres
def mood_to_genres(mood):
    genre_map = {
        "happy": ["pop", "dance-pop", "electronic"],
        "sad": ["indie", "acoustic", "alternative"],
        "chill": ["chill", "lo-fi", "ambient"],
        "hype": ["hip-hop", "electronic", "pop"],
        "romantic": ["r-n-b", "soul", "pop"]
    }
    return genre_map.get(mood, ["pop", "indie"])

# Ask for vibe
prompt = input("What's the vibe? > ")
if not prompt.strip():
    print("❌ No vibe provided. Exiting.")
    exit()

mood = detect_mood_from_prompt(prompt)
features = mood_to_features[mood]
genres = mood_to_genres(mood)

print(f"🎯 Detected mood: {mood}")
print(f"🎶 Using genre seeds: {', '.join(genres)}")

# Get recommendations directly
try:
    recommendations = sp.recommendations(
        seed_genres=genres,
        limit=30,
        target_valence=features["valence"],
        target_energy=features["energy"],
        target_tempo=features["tempo"]
    )
except Exception as e:
    print(f"❌ Failed to get recommendations: {e}")
    exit()

tracks = recommendations.get("tracks", [])
track_uris = [track["uri"] for track in tracks]

if not track_uris:
    print("⚠️ No tracks found matching your vibe. Try a different prompt!")
    exit()

# Create playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"House of Playlist - {mood.title()} Vibes",
    public=True,
    description=f"Generated from prompt: '{prompt}'"
)
sp.playlist_add_items(playlist["id"], track_uris)

# Done
print("✅ Playlist created!")
print("🎧 Playlist URL:", playlist["external_urls"]["spotify"])