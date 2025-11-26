# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025

import streamlit as st
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Spotify playlist mapping (official curated playlists)
PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",  # Sad Songs
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",  # Rock/Intense
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",  # Chill Vibes
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",  # Energetic
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",  # Dark/Spooky
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"   # Heavy
}
# --- END CONFIGURATION ---

# --- SIMULATED COMPUTER VISION ANALYSIS ---
def analyze_image_for_cv_features(image_file):
    """
    SIMULATION FUNCTION: In a real application, this is where you would call
    your trained Computer Vision models (e.g., Keras/TensorFlow model) to:
    1. Detect if a mask is present.
    2. Detect the emotion and its confidence level.
    """
    # 1. Simulate Mask Detection
    # Roughly 20% chance of detecting a mask in the simulation
    mask_present = random.random() < 0.2
    
    # 2. Simulate Emotion Detection and Confidence
    mood = random.choice(list(PLAYLISTS.keys()))
    # Confidence level between 0.60 and 0.99
    confidence = round(random.uniform(0.60, 0.99), 2)
    
    return mood, confidence, mask_present
# --- END SIMULATION ---

# --- APP LAYOUT ---

st.title("EmoPlay 🎶")
st.markdown("### Let your face choose the music")
st.write("Take a selfie or select your current mood — matching Spotify playlist starts instantly.")

# Camera input
img_file = st.camera_input("📸 Take a selfie for automatic mood detection")
mood = None # Initialize mood variable

if img_file:
    # Display captured image
    st.image(img_file, use_column_width=True)
    
    # Run the simulated analysis
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file)

    if mask_present:
        # **NEW FEATURE: Mask Warning**
        st.warning(
            "⚠️ **Mask Detected!** Emotion detection may be unreliable. "
            "Please remove your mask for accurate analysis or select your mood manually."
        )
        mood = st.selectbox("How are you feeling right now?", options=list(PLAYLISTS.keys()), index=3)
        st.info("Using manually selected mood.")

    else:
        # Display the result if no mask is detected
        mood = detected_mood
        st.success(f"✅ Detected mood: **{mood.upper()}**")
        
        # **NEW FEATURE: Confidence Level Meter**
        st.metric(label="Detection Confidence", value=f"{int(confidence*100)}%")
        st.progress(confidence, text="Confidence Level")

else:
    st.info("Or select your mood manually below")
    # Manual mood selection is the fallback
    mood = st.selectbox("How are you feeling right now?", options=list(PLAYLISTS.keys()), index=3)

# Display and play the matching playlist
if mood:
    st.markdown("---")
    st.markdown("### Now Playing ▶️")
    st.components.v1.iframe(PLAYLISTS[mood], height=380)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Full ML + Live Webcam version available on Google Colab")
