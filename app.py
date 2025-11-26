# app.py - EmoPlay (Guaranteed Working on Streamlit Cloud)
import os
os.environ["OPENCV_VIDEOIO_MSPF_DISABLE"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import os

# Critical fixes for Streamlit Cloud
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["OPENCV_VIDEOIO_MSPF_DISABLE"] = "1"

st.set_page_config(page_title="EmoPlay", layout="centered")

st.title("EmoPlay")
st.markdown("### _Your face chooses the music_")

PLAYLISTS = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

img_file = st.camera_input("Take a selfie")

if img_file:
    st.image(img_file, use_column_width=True)
    bytes_data = img_file.getvalue()
    frame = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    with st.spinner("Detecting emotion..."):
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False,
                                             detector_backend="opencv", silent=True)[0]
            mood = result["dominant_emotion"].lower()

            st.success(f"Detected: **{mood.upper()}**")

            st.markdown("#### Emotion Percentages")
            for emo, val in result["emotion"].items():
                st.write(f"{emo.capitalize()}: {val:.1f}%")
                st.progress(val/100)

            # Simple mask/glasses warning
            if val < 30 and emo in ["happy", "sad"]:
                st.warning("Low confidence — Remove mask/glasses for better result")

        except:
            st.error("No face detected. Try again!")
            mood = "neutral"
else:
    mood = st.selectbox("Select mood", list(PLAYLISTS.keys()), index=3)

st.components.v1.iframe(PLAYLISTS[mood], height=380)
st.caption("Built by Vazir • B.Tech CSE 2025 | Real AI Emotion Detection")
