# app.py — Streamlit version for AI Playlist Generator (genre-based only)

import streamlit as st
from mood_parser import detect_mood_from_prompt, mood_to_features
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from valid_genres import VALID_SPOTIFY_GENRES

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private user-library-read"
))

# Mood to genre mapping
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

# UI setup
st.title("🎶 House of Playlist")
st.subheader("Turn your vibe into a Spotify playlist")

# Sidebar toggle
with st.sidebar:
    if st.checkbox("Show valid Spotify genres"):
        st.write(", ".join(sorted(VALID_SPOTIFY_GENRES)))

# Input prompt
prompt = st.text_input("What's the vibe?")

if st.button("Generate Playlist"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        st.write("🧠 Analyzing mood...")
        mood = detect_mood_from_prompt(prompt)
        genres = mood_to_genres(mood)

        st.success(f"Detected mood: **{mood}**")
        st.write(f"Using genre: `{genres[0]}`")

        # Search tracks via genre
        try:
            results = sp.search(q=f"genre:{genres[0]}", type="track", limit=30)
            tracks = results["tracks"]["items"]
            uris = [track["uri"] for track in tracks]
        except Exception as e:
            st.error(f"Spotify search failed: {e}")
            uris = []

        if not uris:
            st.warning("No songs found.")
        else:
            user = sp.current_user()
            playlist = sp.user_playlist_create(
                user=user["id"],
                name=f"House of Playlist - {mood.title()} Vibes",
                public=True,
                description=f"Generated from prompt: '{prompt}'"
            )
            sp.playlist_add_items(playlist["id"], uris)

            st.success("✅ Playlist created!")
            st.markdown(f"[🎧 Listen on Spotify]({playlist['external_urls']['spotify']})")