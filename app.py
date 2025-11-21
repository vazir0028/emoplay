import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("EmoPlay – Music According to Your Mood")
st.markdown("**Camera on karo → mood detect hoga → songs change ho jayenge!**")

playlists = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

img_file = st.camera_input("Take a picture")

if img_file is not None:
    img = Image.open(img_file)
    img_array = np.array(img)

    with st.spinner("Detecting mood..."):
        try:
            emotion = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False, silent=True)[0]['dominant_emotion']
        except:
            emotion = "neutral"

    st.image(img, caption=f"Detected → {emotion.upper()}", use_column_width=True)
    st.success(f"You are feeling **{emotion.upper()}**")
    st.write("### Now Playing Songs For Your Mood")
    st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380)
else:
    st.info("Camera on karo bhai!")

st.caption("Made by Vazir | BTech CSE 2025")
