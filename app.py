import streamlit as st
import face_recognition
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("🎵 EmoPlay – Music That Matches Your Mood (Light Version)")
st.write("**Camera on karo → Mood detect (via face landmarks) → Songs change!**")

# Spotify playlists
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

# Simple emotion from landmarks (smile detection for happy, etc.)
def detect_emotion(image_array):
    try:
        face_landmarks = face_recognition.face_landmarks(image_array)
        if not face_landmarks:
            return "neutral"
        
        # Basic smile detection (distance between mouth corners)
        landmarks = face_landmarks[0]
        mouth_left = landmarks['bottom_lip'][2]  # Left mouth corner
        mouth_right = landmarks['bottom_lip'][6]  # Right mouth corner
        mouth_distance = np.linalg.norm(np.array(mouth_left) - np.array(mouth_right))
        
        if mouth_distance > 0.02:  # Threshold for smile (tune if needed)
            return "happy"
        elif mouth_distance < 0.01:
            return "sad"
        else:
            return "neutral"
    except:
        return "neutral"

img_file = st.camera_input("📸 Take a selfie")

if img_file is not None:
    image = Image.open(img_file)
    img_array = np.array(image)
    
    with st.spinner("🔍 Detecting emotion..."):
        emotion = detect_emotion(img_array)
    
    st.image(image, caption=f"Detected: {emotion.upper()}", use_column_width=True)
    st.success(f"🎭 Mood: **{emotion.upper()}**")
    st.write("### 🎶 Now Playing Songs For Your Mood")
    st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380)
else:
    st.info("👆 Camera allow karo!")

st.caption("Made by Vazir | BTech CSE | Alternative: face_recognition lib")
