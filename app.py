# app.py → EmoPlay by Vazir (BTech CSE)
import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image

# Page title & style
st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("EmoPlay – Music According to Your Mood")
st.markdown("**Allow camera → Look at webcam → Songs change with your emotion!**")

# Spotify mood playlists (public links – no login needed)
playlists = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",  # Happy hits
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",  # Sad songs
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",  # Angry/Rock
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",  # Chill
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",  # Energetic
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",  # Spooky
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"   # Heavy
}

# Camera input
img_file = st.camera_input(" ")

if img_file is not None:
    # Load image
    image = Image.open(img_file)
    img_array = np.array(image)

    # Detect emotion
    with st.spinner("Detecting your mood..."):
        try:
            result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False, silent=True)
            emotion = result[0]['dominant_emotion']
        except:
            emotion = "neutral"

    # Show result
    st.image(image, caption=f"Detected Mood → {emotion.upper()}", use_column_width=True)
    st.success(f"Feeling **{emotion.upper()}** right now!")
    
    # Play matching playlist
    st.write("### Now Playing Songs For Your Mood")
    st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380)

else:
    st.info("Camera on karo aur mood check karo!")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by **Vazir** | BTech CSE | 2025")
