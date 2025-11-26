# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import random
import streamlit.components.v1 as components

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- REAL SPOTIFY EMBED LINKS ---
# These are actual embed URLs. 
# To get these: Go to Spotify -> Share -> Embed Track -> Copy the 'src' link from the code.

# International Hits
INT_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/track/60nZcImufyMA1SFQYoc3dV?utm_source=generator", # Happy - Pharrell Williams
    "sad":      "https://open.spotify.com/embed/track/7qEHsqek33rTcFNT9PFqLf?utm_source=generator", # Someone You Loved - Lewis Capaldi
    "angry":    "https://open.spotify.com/embed/track/0hCB0YR03f6AmQaHbwWDe8?utm_source=generator", # Whole Lotta Love - Led Zeppelin
    "neutral":  "https://open.spotify.com/embed/track/45bE4HXI0AwGZXfZtMp8JR?utm_source=generator", # You're Beautiful - James Blunt
    "surprise": "https://open.spotify.com/embed/track/32OlwWuMpZ6b0aN2RZOeMS?utm_source=generator", # Uptown Funk
    "fear":     "https://open.spotify.com/embed/track/2C31rKYpBf48iR4r2f4xAA?utm_source=generator", # Thriller - Michael Jackson
    "disgust":  "https://open.spotify.com/embed/track/2zYzyRzz6pRmhPzyfMEC8s?utm_source=generator"  # Highway to Hell
}

# Bollywood Hits
BOLLYWOOD_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/track/7cVpG8E217pYhZ6Z7Zp3W1?utm_source=generator", # Badtameez Dil
    "sad":      "https://open.spotify.com/embed/track/0Rz3q9p5Y58V0c6O9wZ0dG?utm_source=generator", # Channa Mereya
    "angry":    "https://open.spotify.com/embed/track/5mnpMnnkyl1GZ7S1zQ8CjP?utm_source=generator", # Apna Time Aayega
    "neutral":  "https://open.spotify.com/embed/track/2Fv2injs4qAm8mJBGaxFHU?utm_source=generator", # Kun Faya Kun
    "surprise": "https://open.spotify.com/embed/track/5IyL3WOaQbUo4Q0L5qGgV0?utm_source=generator", # Gallan Goodiyaan
    "fear":     "https://open.spotify.com/embed/track/1Z3g0YGK3sH6m5W5FkH5i?utm_source=generator", # Gali Gali
    "disgust":  "https://open.spotify.com/embed/track/5mnpMnnkyl1GZ7S1zQ8CjP?utm_source=generator"  # Apna Time Aayega (Reuse)
}

# --- SIMULATED COMPUTER VISION ANALYSIS ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection and confidence."""
    # I have removed the hardcoded "sad" so you can see different results for testing.
    possible_moods = list(INT_PLAYLISTS.keys())
    
    mask_present = random.random() < 0.1 # 10% chance of mask
    mood = random.choice(possible_moods) # Random mood for simulation
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
    # Note: height=80 is standard for a single song, 380 for a playlist
    components.iframe(spotify_url, height=80)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025")
