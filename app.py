import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("🎵 EmoPlay – Music That Matches Your Mood")
st.write("**Camera on karo → Smile/Sad/Angry karo → Songs change ho jayenge!**")

# Spotify playlists for moods
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
img_file = st.camera_input("📸 Take a selfie for mood detection")

if img_file is not None:
    # Load image
    image = Image.open(img_file)
    img_array = np.array(image)

    # Detect emotion
    with st.spinner("🔍 Detecting your mood..."):
        try:
            result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False, silent=True)
            emotion = result[0]['dominant_emotion']
        except Exception as e:
            st.error(f"Error detecting mood: {e}")
            emotion = "neutral"

    # Show results
    st.image(image, caption=f"Detected Mood: {emotion.upper()}", use_column_width=True)
    st.success(f"🎭 You are feeling **{emotion.upper()}**!")
    
    # Play playlist
    st.write("### 🎶 Now Playing: Songs for Your Mood")
    st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380, scrolling=False)

else:
    st.info("👆 Camera allow karo aur photo lo – mood detect hoga!")

# Footer
st.markdown("---")
st.caption("✨ Made by **Vazir** | BTech CSE | Machine Learning Project 2025")
