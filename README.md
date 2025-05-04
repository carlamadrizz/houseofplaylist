# AI Playlist Generator – House of Playlist

A simple AI tool that turns mood-based text input (like “hype gym workout” or “chill study vibe”) into a custom Spotify playlist — using only **genre search** due to Spotify API limitations.

---

## Features

- Text-based mood detection (e.g., `"rainy breakup"`, `"happy picnic"`)
- Heuristic mapping of moods to Spotify-supported genres
- Playlist generation via **Spotify Search API** (not recommendations)
- Two interfaces:
  - ✅ `Streamlit` for interactive browser use
  - ✅ `Command Line` for quick testing

---

## Spotify API Limitations (As of May 2025)

Due to recent deprecations by Spotify:

| Deprecated Feature          | Status             | Impact                                                  |
| --------------------------- | ------------------ | ------------------------------------------------------- |
| `/recommendations` endpoint | 🔴 Deprecated      | Cannot generate playlists using valence/energy directly |
| `/audio-features` endpoint  | 🔴 Deprecated/403s | Cannot filter tracks based on audio features            |
| `/search` endpoint          | ✅ Still Supported | Used to find songs by genre                             |

As a result, our app now uses only **genre-based filtering**, which is less accurate than audio features but still functional.

---

## File Overview

| File               | Description                                        |
| ------------------ | -------------------------------------------------- |
| `app.py`           | Streamlit app — interactive mood-to-playlist UI    |
| `main.py`          | CLI app — generates playlists from command line    |
| `mood_parser.py`   | Converts user prompts into mood + genre heuristics |
| `valid_genres.py`  | List of Spotify-allowed seed genres (filtered)     |
| `.env.example`     | Template for your Spotify credentials              |
| `requirements.txt` | Python dependencies (e.g., `spotipy`, `streamlit`) |

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. **Create and activate a virtual environment**

python -m venv venv
source venv/bin/activate # macOS/Linux
.\venv\Scripts\activate # Windows

3. **Insall dependencies**

pip install -r requirements.txt

4. **Set up your environment**

create a file .env then edit and add your

CLIENT_ID=
CLIENT_SECRET=

---

## How To Run

Streamlit Web App

- streamlit run app.py

OR

CLI

- python main.py
