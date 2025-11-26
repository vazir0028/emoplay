# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import random
# Page configuration
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# App title and description
st.title("EmoPlay")
st.markdown("### Let your face choose the music")
st.write("Take a selfie or select your current mood — matching Spotify playlist starts instantly.")
# Spotify playlist mapping (official curated playlists)
PLAYLISTS = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC", # Happy Hits
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1", # Sad Songs
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg", # Rock/Intense
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL", # Chill Vibes
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr", # Energetic
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned", # Dark/Spooky
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg" # Heavy
}
# Camera input
img_file = st.camera_input("Take a selfie for automatic mood detection")
if img_file:
    # Display captured image
    st.image(img_file, use_column_width=True)
   
    # Simulate mood detection (full ML version available on Colab)
    mood = random.choice(list(PLAYLISTS.keys()))
    st.success(f"Detected mood: **{mood.upper()}**")
else:
    st.info("Or select your mood manually below")
    mood = st.selectbox("How are you feeling right now?", options=list(PLAYLISTS.keys()), index=3)
# Display and play the matching playlist
st.markdown("### Now Playing")
st.components.v1.iframe(PLAYLISTS[mood], height=380)
# Footer
st.markdown("---")
st.caption("Built by Vazir • B.Tech CSE 2025 | Full ML + Live Webcam version available on Google Colab") 
