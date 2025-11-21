import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("🎵 EmoPlay – Music That Matches Your Mood")
st.markdown("**Camera on karo → Smile/Sad/Angry try karo → Songs auto change!**")

# Spotify playlists for different moods
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

# Camera input
img_file = st.camera_input("📸 Take a selfie for emotion detection")

if img_file is not None:
    # Load image from camera
    image = Image.open(img_file)
    img_array = np.array(image)

    # Detect emotion with fixed backend (opencv = fast & no conflict)
    with st.spinner("🔍 Detecting your emotion..."):
        try:
            result = DeepFace.analyze(
                img_array, 
                actions=['emotion'], 
                enforce_detection=False, 
                silent=True,
                detector_backend='opencv'  # Yeh fix hai – retinaface ki jagah opencv use kar rahe hain
            )
            emotion = result[0]['dominant_emotion']
        except Exception as e:
            st.error(f"Detection error: {e}")
            emotion = "neutral"

    # Display results
    st.image(image, caption=f"Detected Emotion: {emotion.upper()}", use_column_width=True)
    st.success(f"🎭 You're feeling **{emotion.upper()}** right now!")
    
    # Play matching Spotify playlist
    st.write("### 🎶 Now Playing: Perfect Songs For Your Mood")
    playlist_url = playlists.get(emotion.lower(), playlists["neutral"])
    st.components.v1.iframe(playlist_url, height=380, scrolling=False)

else:
    st.info("👆 Camera allow karo aur ek photo lo – mood detect hoga!")

# Project footer
st.markdown("---")
st.caption("✨ Built by **Vazir** | BTech CSE | ML Project 2025 | Tech: DeepFace + Streamlit + Spotify")
