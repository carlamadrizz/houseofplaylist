# Spotify-compatible audio feature mappings for each mood
mood_to_features = {
    "sad":       {"valence": 0.2, "energy": 0.3, "tempo": 70},
    "happy":     {"valence": 0.9, "energy": 0.8, "tempo": 120},
    "chill":     {"valence": 0.5, "energy": 0.4, "tempo": 85},
    "hype":      {"valence": 0.8, "energy": 0.95, "tempo": 135},
    "angry":     {"valence": 0.3, "energy": 1.0, "tempo": 150},
    "romantic":  {"valence": 0.8, "energy": 0.4, "tempo": 100},
    "nostalgic": {"valence": 0.4, "energy": 0.3, "tempo": 75},
    "focused":   {"valence": 0.6, "energy": 0.3, "tempo": 80},
    "melancholy":{"valence": 0.3, "energy": 0.2, "tempo": 65},
    "motivated": {"valence": 0.85, "energy": 0.9, "tempo": 125},
    "relaxed":   {"valence": 0.6, "energy": 0.3, "tempo": 85}
}

# Keywords matched from user prompt to detect mood
def detect_mood_from_prompt(prompt):
    prompt = prompt.lower()

    if any(word in prompt for word in ["cry", "sad", "alone", "heartbreak", "depressed"]):
        return "sad"
    elif any(word in prompt for word in ["happy", "excited", "sunny", "uplifting", "joy"]):
        return "happy"
    elif any(word in prompt for word in ["chill", "vibe", "lofi", "study", "calm"]):
        return "chill"
    elif any(word in prompt for word in ["hype", "party", "workout", "energy", "pump"]):
        return "hype"
    elif any(word in prompt for word in ["angry", "mad", "rage", "revenge"]):
        return "angry"
    elif any(word in prompt for word in ["love", "crush", "romance", "date"]):
        return "romantic"
    elif any(word in prompt for word in ["remember", "past", "miss", "old days"]):
        return "nostalgic"
    elif any(word in prompt for word in ["focus", "work", "deep", "concentration"]):
        return "focused"
    elif any(word in prompt for word in ["melancholy", "blue", "quiet sad"]):
        return "melancholy"
    elif any(word in prompt for word in ["grind", "goal", "push", "determined"]):
        return "motivated"
    elif any(word in prompt for word in ["relax", "breathe", "soothing", "calm"]):
        return "relaxed"
    else:
        return "chill"

# Valid Spotify seed genres as of May 2025
VALID_GENRES = {
    "acoustic", "ambient", "blues", "classical", "club", "country", "dance", "disco",
    "edm", "electro", "electronic", "folk", "funk", "gospel", "grunge", "happy", "hip-hop",
    "house", "indie", "jazz", "k-pop", "latin", "metal", "party", "piano", "pop", "punk",
    "r-n-b", "reggae", "rock", "romance", "soul", "study", "techno", "trance", "trip-hop", "work-out"
}

# Map each mood to Spotify-safe genres
def mood_to_genres(mood):
    genre_map = {
        "happy":      ["pop", "dance", "electronic"],
        "sad":        ["acoustic", "piano", "indie"],
        "chill":      ["ambient", "study", "piano"],
        "hype":       ["hip-hop", "edm", "work-out"],
        "angry":      ["metal", "rock", "punk"],
        "romantic":   ["r-n-b", "soul", "romance"],
        "nostalgic":  ["indie", "acoustic", "folk"],
        "focused":    ["study", "ambient", "electronic"],
        "melancholy": ["piano", "blues", "acoustic"],
        "motivated":  ["pop", "hip-hop", "edm"],
        "relaxed":    ["lofi", "ambient", "jazz"]
    }

    fallback = ["pop"]
    selected = genre_map.get(mood, fallback)
    filtered = [g for g in selected if g in VALID_GENRES]
    return filtered if filtered else fallback
# Test locally via CLI
if __name__ == "__main__":
    prompt = input("What's the vibe? > ")
    mood = detect_mood_from_prompt(prompt)
    print("🎯 Detected mood:", mood)
    print("🧪 Target features:", mood_to_features[mood])
    print("🎵 Valid genres:", mood_to_genres(mood))
