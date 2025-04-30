

mood_to_features = {
    "sad":    {"valence": 0.2, "energy": 0.3, "tempo": 70},
    "happy":  {"valence": 0.9, "energy": 0.8, "tempo": 120},
    "chill":  {"valence": 0.5, "energy": 0.4, "tempo": 85},
    "hype":   {"valence": 0.8, "energy": 0.95, "tempo": 135},
    "angry":  {"valence": 0.3, "energy": 1.0, "tempo": 150},
}

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
    else:
        return "chill"  # fallback default
    
if __name__ == "__main__":
    prompt = input("What's the vibe? > ")
    mood = detect_mood_from_prompt(prompt)
    print("🎯 Detected mood:", mood)
    print("🧪 Target features:", mood_to_features[mood])

