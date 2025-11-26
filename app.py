%%writefile app.py
import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EmoBeats - AI Music Player",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    h1 {
        color: #1DB954; /* Spotify Green */
        text-align: center;
    }
    .stButton>button {
        color: white;
        background-color: #1DB954;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- PLAYLIST CONFIGURATION ---
INT_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1EIeCX1SSo6M9y",
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM",
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX186v583rmzp"
}

BOLLYWOOD_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM", # Bollywood Dance
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DXca8AM0c05a1", # Bollywood Sad
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DX7sI57iHQdM6", # Workout
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DXd8cOUiya1cg", # Acoustic
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM", # Party
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1", # Horror
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX186v583rmzp"  # Heavy
}

# --- APP LAYOUT ---
st.title("🎵 EmoBeats AI")
st.markdown("### Let your face choose the music")

# 1. Genre Selection
genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1 
)

CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

st.write("Take a selfie below to detect your mood!")

# 2. Camera Input
img_file = st.camera_input("📸 Camera")

# 3. Logic Flow
if img_file is not None:
    # Convert buffer to Image for OpenCV
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Analyze with DeepFace
    with st.spinner("🧠 AI is analyzing your face..."):
        try:
            # The Magic happens here
            result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False, silent=True)
            detected_mood = result[0]['dominant_emotion']
            confidence = result[0]['emotion'][detected_mood]
            
            # Display Result
            st.success(f"✅ Detected: **{detected_mood.upper()}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence", f"{confidence:.1f}%")
            with col2:
                st.metric("Genre", genre_choice)
                
            st.progress(int(confidence), text="AI Confidence Level")

            # Show Player
            st.markdown("---")
            st.subheader(f"🎵 Now Playing: {detected_mood.title()} Vibes")
            
            playlist_url = CURRENT_PLAYLISTS.get(detected_mood, CURRENT_PLAYLISTS["neutral"])
            components.iframe(playlist_url, height=400)

        except Exception as e:
            st.error("⚠️ Face not detected! Try getting closer to the camera.")
            st.write(f"Error details: {e}")

else:
    st.info("Waiting for photo...")
    # Optional: Manual override
    with st.expander("Or select mood manually"):
        manual_mood = st.selectbox("Pick a mood", list(CURRENT_PLAYLISTS.keys()))
        if st.button("Play Manual"):
            components.iframe(CURRENT_PLAYLISTS[manual_mood], height=400)

st.markdown("---")
st.caption("Built by Prem 2025 | Powered by DeepFace & Streamlit")
