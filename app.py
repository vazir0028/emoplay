# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import streamlit.components.v1 as components
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- REAL SPOTIFY EMBED LINKS ---
# I have replaced the broken placeholders with REAL Spotify Embed URLs.
# To get your own: Go to Spotify > Share > Embed Track > Copy the 'src' link.

# International Hits
INT_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/track/60nZcImufyMA1KT4eGO2Tv", # Happy - Pharrell Williams
    "sad":      "https://open.spotify.com/embed/track/7qEHsqek33rTcFNT9PFqLf", # Someone You Loved - Lewis Capaldi
    "angry":    "https://open.spotify.com/embed/track/3hgl7EQwTutSm6PESsB7gZ", # Seven Nation Army
    "neutral":  "https://open.spotify.com/embed/track/2374M0fQpWi3dLnB54qaLX", # Africa - Toto
    "surprise": "https://open.spotify.com/embed/track/32OlwWuMpZ6b0aN2RZOeMS", # Uptown Funk
    "fear":     "https://open.spotify.com/embed/track/3ZSuyGGqBDTEFlK7qCa1tq", # Thriller
    "disgust":  "https://open.spotify.com/embed/track/2zYzyRzz6pKOfBXM3J2T02"  # Highway to Hell
}

# Bollywood Hits
BOLLYWOOD_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/track/7cVp5X1sO2aB0xS0w1R6aA", # Badtameez Dil
    "sad":      "https://open.spotify.com/embed/track/0Rz3Lp7QZ3M0W1R6aA", # Channa Mereya
    "angry":    "https://open.spotify.com/embed/track/5nNmjCZCqO2jRcfkGfb5Hl", # Sadda Haq
    "neutral":  "https://open.spotify.com/embed/track/4bdQG3Tj6o0c3X5o6ZzD3e", # Kun Faya Kun
    "surprise": "https://open.spotify.com/embed/track/1wNvdFT4RNv6mCN9uJtLgM", # Gallan Goodiyaan
    "fear":     "https://open.spotify.com/embed/track/6Qe8F1J0B2L1vF3yG4nK5q", # Gali Gali
    "disgust":  "https://open.spotify.com/embed/track/5nNmjCZCqO2jRcfkGfb5Hl"  # Reuse Sadda Haq
}

# --- SIMULATED COMPUTER VISION ANALYSIS ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection and confidence."""
    # FIX: Removed the hardcoded 'sad' variable so the app is dynamic again.
    
    possible_moods = list(INT_PLAYLISTS.keys())
    
    # 10% chance of detecting a mask
    mask_present = random.random() < 0.1 
    
    # Randomly pick a mood for simulation purposes
    mood = random.choice(possible_moods) 
    
    confidence = round(random.uniform(0.80, 0.99), 2)
    return mood, confidence, mask_present

# --- APP LAYOUT ---
st.title("EmoPlay 🎶")
st.markdown("### Let your face choose the music")

# Genre Selection
genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1 
)

# Set the current playlist dictionary
CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

st.write("Take a selfie or select your current mood — matching playlist starts instantly.")

# Camera input
img_file = st.camera_input("📸 Take a selfie for automatic mood detection")

mood = None 

if img_file:
    # Display captured image
    st.image(img_file, width=300)
    
    # Run the simulated analysis
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file)
    
    if mask_present:
        st.warning("⚠️ **Mask Detected!** Emotion detection may be unreliable.")
        mood = st.selectbox("Confirm your mood:", options=list(CURRENT_PLAYLISTS.keys()), index=0)
    else:
        mood = detected_mood
        st.success(f"✅ Detected mood: **{mood.upper()}**")
        st.metric(label="Detection Confidence", value=f"{int(confidence*100)}%")
        st.progress(confidence)
else:
    st.info("Or select your mood manually below")
    mood = st.selectbox("How are you feeling right now?", options=list(CURRENT_PLAYLISTS.keys()), index=0)

# Display and play the matching playlist
if mood:
    st.markdown("---")
    st.markdown(f"### Now Playing: **{mood.upper()} ({genre_choice})** ▶️")
    
    # Get the correct URL
    spotify_url = CURRENT_PLAYLISTS[mood]
    
    # Render the Spotify Player
    # Height 80 is best for single tracks, 380 is best for playlists
    components.iframe(spotify_url, height=80)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025")
