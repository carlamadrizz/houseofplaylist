import streamlit as st
from mood_parser import get_genres_for_input
from dotenv import load_dotenv
import os
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth

# Load .env
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Setup Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private",
    cache_path=".cache"
))

# UI
st.title("AI Playlist Generator")
st.subheader("Describe your vibe, get a custom Spotify playlist.")

prompt = st.text_input("How are you feeling today?")

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please describe your vibe.")
    else:
        st.write("Analyzing...")
        mood, genres = get_genres_for_input(prompt)
        selected_genre = random.choice(genres) if genres else "pop"

        st.success(f"Mood: **{mood}**")
        st.write(f"🎵 Using genre: `{selected_genre}`")

        try:
            results = sp.search(q=f"genre:{selected_genre}", type="track", limit=30)
            tracks = results["tracks"]["items"]
            uris = [t["uri"] for t in tracks]
        except Exception as e:
            st.error(f"Spotify search failed: {e}")
            uris = []

        if not uris:
            st.warning("No tracks found.")
        else:
            user = sp.current_user()
            playlist = sp.user_playlist_create(
                user=user["id"],
                name=f"{mood.title()} Vibes",
                public=True,
                description=f"Generated from: {prompt}"
            )
            sp.playlist_add_items(playlist["id"], uris)
            st.success("Playlist created!")
            st.markdown(f"[Listen on Spotify]({playlist['external_urls']['spotify']})")