# AI Playlist Generator – House of Playlist

A lightweight AI tool that takes mood-based text input (like “feeling kinda down” or “chill study grind”) and turns it into a Spotify playlist — powered by symbolic AI and limited to genre-based search due to Spotify API constraints.

---

## What Makes This Project “AI”?

This system uses a **two-part symbolic AI pipeline**:

### 1. **Sentiment Detection with TextBlob**

- We use [TextBlob](https://textblob.readthedocs.io/en/dev/) to analyze the user's prompt for:
  - **Polarity** (positive ↔ negative)
  - **Subjectivity** (objective ↔ emotional)
- This replaces the need for a hand-coded dictionary or weighted keyword list (time constraint due Friday).

### 2. **Rule-Based Heuristic Logic (Our AI Contribution)**

- Based on the TextBlob sentiment output, we apply **custom logic** to classify the input into moods:
  - `happy`, `sad`, `depressed`, `chill`, `motivated`, `emotional`, `neutral`
- Each mood is mapped to a curated list of **Spotify-supported genres**
- A genre is then **randomly selected** to avoid repetition

> Example:  
> “Feeling really down lately” → Polarity: -0.6 → Mood: `depressed` → Genre: randomly chosen from `["blues", "singer-songwriter", "ambient", ...]`

This system demonstrates explainable, rule-based symbolic AI

---

## Spotify API Limitations

Due to recent changes in Spotify’s developer tools:

| Feature            | Status     | Impact                                                  |
| ------------------ | ---------- | ------------------------------------------------------- |
| `/recommendations` | Deprecated | Can't use valence/energy-based recommendation filtering |
| `/audio-features`  | 403 Errors | Can't sort songs by danceability, tempo, energy, etc.   |
| `/search`          | Supported  | We use this to search for songs by genre                |

Because of this, **genre-based search** is our only reliable playlist method.

---

## Known Issues & Limitations

- **Short or slang-based inputs** (e.g., `"I'm hyped"`) can be misclassified by TextBlob, since it lacks context understanding.
- The AI may label something as `"emotional"` when the user intended `"motivated"` or `"hype"`.
- Random genre selection can occasionally produce unexpected (but still technically valid) results like `opera` for `"emotional"`.

These limitations are intentional trade-offs for keeping the system **symbolic, explainable, and lightweight**.

---

## File Overview

| File               | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `main.py`          | CLI version – generates playlists from terminal              |
| `app.py`           | Streamlit web app – clean UI for mood-to-playlist generation |
| `mood_parser.py`   | TextBlob sentiment + our custom mood-to-genre AI logic       |
| `valid_genres.py`  | List of Spotify-supported genres                             |
| `.env.example`     | Template for setting your Spotify credentials                |
| `requirements.txt` | Python dependencies (TextBlob, Spotipy, Streamlit, etc.)     |

---

## Setup Instructions

1. **Create and activate a virtual environemnt**
   python -m venv venv
   source venv/bin/activate # macOS/Linux
   .\venv\Scripts\activate # Windows

2. **Install dependencies**
   pip install -r requirements.txt

3. **Add your spotify credentials**
   create a .env file with:
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret

4. **How to run**
   Streamlit Web App:
   streamlit run app.py

   CLI
   python main.py