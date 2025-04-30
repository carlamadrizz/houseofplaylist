import streamlit as st
from mood_parser import detect_mood_from_prompt, mood_to_features
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-public playlist-modify-private user-read-private user-library-read"

))

# Helper: choose genre seeds based on mood
def mood_to_genres(mood):
    genre_map = {
        "happy": ["pop", "dance-pop", "electronic"],   # FIXED
        "sad": ["indie", "acoustic", "alternative"],
        "chill": ["chill", "lo-fi", "ambient"],
        "hype": ["hip-hop", "electronic", "pop"],
        "romantic": ["r-n-b", "soul", "pop"]
    }
    return genre_map.get(mood, ["pop", "indie"])


# Streamlit UI
st.title("🎶 House of Playlist")
st.subheader("Turn your vibe into a Spotify playlist")

prompt = st.text_input("What's the vibe?", "")

if st.button("Generate Playlist"):
    if prompt.strip() == "":
        st.warning("Please enter a vibe prompt.")
    else:
        st.write("🧠 Analyzing mood...")
        mood = detect_mood_from_prompt(prompt)
        features = mood_to_features[mood]
        genres = mood_to_genres(mood)

        st.success(f"Detected mood: **{mood}**")
        st.write(f"Using genre seeds: {', '.join(genres)}")

        # Get recommendations based on features
        try:
            recommendations = sp.recommendations(
                seed_genres=genres,
                limit=30,
                target_valence=features["valence"],
                target_energy=features["energy"],
                target_tempo=features["tempo"]
            )
        except Exception as e:
            st.error(f"Failed to get recommendations: {e}")
            recommendations = {"tracks": []}

        tracks = recommendations.get("tracks", [])
        track_uris = [track["uri"] for track in tracks]

        if not track_uris:
            st.warning("No recommendations found — try a different vibe.")
        else:
            user = sp.current_user()
            playlist = sp.user_playlist_create(
                user=user["id"],
                name=f"House of Playlist - {mood.title()} Vibes",
                public=True,
                description=f"Auto-generated from vibe: '{prompt}'"
            )
            sp.playlist_add_items(playlist["id"], track_uris)

            st.success("✅ Playlist created!")
            st.markdown(f"[🎧 Listen on Spotify]({playlist['external_urls']['spotify']})")