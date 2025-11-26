# app.py - EmoPlay: Emotion-Based Music Player (Upgraded Version)
# Author: Vazir | B.Tech CSE 2025

import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import os

# Reduce TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Page config
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title
st.title("🎭 EmoPlay")
st.markdown("### _Your face. Your vibe. Your music._")

# Spotify playlists (official curated)
PLAYLISTS = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

# Camera input
img_file = st.camera_input("📸 Take a selfie to detect your mood")

if img_file:
    st.image(img_file, use_column_width=True)
    
    # Convert to OpenCV format
    bytes_data = img_file.getvalue()
    img_array = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    with st.spinner("Analyzing your face..."):
        try:
            # DeepFace analysis with lightweight + fast backend
            result = DeepFace.analyze(
                frame,
                actions=['emotion', 'age', 'gender', 'race'],
                enforce_detection=False,
                detector_backend="opencv",      # Fastest & works everywhere
                silent=True
            )[0]

            mood = result["dominant_emotion"].lower()
            emotions = result["emotion"]

            # === MASK & GLASSES DETECTION ===
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = face_cascade.detectMultiScale(gray, 1.3, 5)

            wearing_mask = False
            wearing_glasses = False

            if len(eyes) == 0:
                # No eyes detected → probably mask or sunglasses
                lower_face = frame[int(frame.shape[0]*0.6):, :]  # Bottom part of face
                if np.mean(lower_face) < 100:  # Very dark → likely mask
                    wearing_mask = True
                else:
                    wearing_glasses = True

            # Show warnings
            if wearing_mask:
                st.error("⚠️ Mask detected! Please remove mask for better accuracy.")
            if wearing_glasses:
                st.warning("🕶️ Glasses/Sunglasses detected → May affect accuracy")

            # Display result
            st.success(f"**Detected Mood: {mood.upper()}**")

            # Show all emotions with progress bars
            st.markdown("#### Emotion Breakdown")
            for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                st.write(f"{emotion.capitalize()}: {score:.1f}%")
                st.progress(score / 100)

        except Exception as e:
            st.error("No face detected 😔 Try better lighting or remove mask/glasses!")
            mood = "neutral"

else:
    st.info("👇 Or select your mood manually")
    mood = st.selectbox("How are you feeling?", options=list(PLAYLISTS.keys()), index=3)

# Play Spotify playlist
st.markdown("### ▶️ Now Playing")
st.components.v1.iframe(PLAYLISTS[mood], height=380)

# Footer
st.markdown("---")
st.caption("🚀 Built by **Vazir** • B.Tech CSE 2025 | Real AI Emotion Detection + Mask/Glasses Alert")
st.markdown("[⭐ Star on GitHub](https://github.com) • [📱 Try on Mobile](https://your-app-link.streamlit.app)")
