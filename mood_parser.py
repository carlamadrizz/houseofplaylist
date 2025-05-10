from textblob import TextBlob
import random

# Step 1: Use TextBlob to analyze sentiment
def analyze_sentiment(user_input):
    blob = TextBlob(user_input)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity
    }

# Step 2: Custom AI logic to classify mood
def classify_mood(polarity, subjectivity):
    if polarity >= 0.6:
        return "happy"
    elif 0.3 <= polarity < 0.6:
        return "chill"
    elif 0.1 <= polarity < 0.3 and subjectivity < 0.5:
        return "motivated"
    elif -0.2 <= polarity < 0.1:
        return "emotional"
    elif -0.5 <= polarity < -0.2:
        return "sad"
    elif polarity < -0.5:
        return "depressed"
    else:
        return "neutral"

# Step 3: Genre mappings (expanded per mood)
MOOD_TO_GENRES = {
    "happy": ["pop", "dance", "latin", "edm", "funk", "salsa"],
    "chill": ["chill", "ambient", "jazz", "lo-fi", "study"],
    "motivated": ["hip-hop", "work-out", "rock", "electronic", "garage"],
    "emotional": ["classical", "romance", "r-n-b", "soundtracks", "opera"],
    "sad": ["acoustic", "piano", "indie", "folk", "blues"],
    "depressed": ["blues", "singer-songwriter", "ambient", "gospel", "slowcore"],
    "neutral": ["instrumental", "study", "sleep", "new-age"]
}

# Final method for integration
def get_genres_for_input(user_input):
    sentiment = analyze_sentiment(user_input)
    mood = classify_mood(sentiment["polarity"], sentiment["subjectivity"])
    genres = MOOD_TO_GENRES.get(mood, ["pop"])
    return mood, genres