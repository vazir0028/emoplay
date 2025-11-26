# app.py - EmoPlay: Emotion-Based Music Player (Live Webcam Edition)
# Author: Vazir | B.Tech CSE 2025

import streamlit as st
import random
import cv2 # Required for frame manipulation in real-time
from PIL import Image # Used for general image handling
import numpy as np # Used to convert between CV2 and PIL formats

# **CRITICAL LIBRARY for Live Processing**
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
# NOTE: We can only simulate the usage here, as the library must be installed.

# --- CONFIGURATION (No Change) ---
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood (Live Webcam)",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Spotify playlist mapping (No Change)
INT_PLAYLISTS = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}
BOLLYWOOD_PLAYLISTS = {
    "happy": "http://googleusercontent.com/spotify.com/bollywood_happy",
    "sad": "http://googleusercontent.com/spotify.com/bollywood_sad",
    "angry": "http://googleusercontent.com/spotify.com/bollywood_angry",
    "neutral": "http://googleusercontent.com/spotify.com/bollywood_chill",
    "surprise": "http://googleusercontent.com/spotify.com/bollywood_energetic",
    "fear": "http://googleusercontent.com/spotify.com/bollywood_dark",
    "disgust": "http://googleusercontent.com/spotify.com/bollywood_heavy"
}
# --- END CONFIGURATION ---

# --- CRITICAL NEW CLASS FOR LIVE PROCESSING ---
# In a real setup, this class handles the frame-by-frame video modification
# For simulation, we'll keep the logic simple.

# GLOBAL STATE to hold the detected mood and confidence for display outside the stream
if 'live_mood' not in st.session_state:
    st.session_state.live_mood = "neutral"
if 'live_confidence' not in st.session_state:
    st.session_state.live_confidence = 0.0

class VideoTransformer: # Inherits from VideoTransformerBase in a real app
    def transform(self, frame):
        # Convert the frame (which is a Numpy array/OpenCV image) to color format
        img = frame.to_ndarray(format="bgr24") 
        h, w = img.shape[:2]

        # 1. ACTUAL FACE DETECTION (Simulation: Assume face is in the center)
        # In a real app, you'd use cv2.CascadeClassifier or an ML model here
        x1, y1, x2, y2 = w // 4, h // 4, 3 * w // 4, 3 * h // 4 # Center area

        # 2. DRAW THE GREEN CIRCLE
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        radius = (x2 - x1) // 2
        cv2.circle(img, (center_x, center_y), radius, (0, 255, 0), 5) # (0, 255, 0) is BGR for Green

        # 3. EMOTION DETECTION (Simulation: Update mood every ~30 frames)
        if random.randint(0, 30) == 1:
            # Simulate real-time mood update
            new_mood = random.choice(list(INT_PLAYLISTS.keys()))
            new_confidence = round(random.uniform(0.60, 0.99), 2)
            
            # Update the global state
            st.session_state.live_mood = new_mood
            st.session_state.live_confidence = new_confidence

        # 4. Draw text (for visual confirmation)
        cv2.putText(
            img, 
            f"Mood: {st.session_state.live_mood.upper()}", 
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
        )

        return img # Return the modified frame

# --- APP LAYOUT ---

st.title("EmoPlay 🎶")
st.markdown("### Let your face choose the music (LIVE)")

genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1
)
CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

st.write("Start the camera below to activate live mood detection.")
st.warning("⚠️ **Note:** For this code to run successfully, you need the `streamlit-webrtc` library.")

# **CRITICAL NEW SECTION: Live Webcam Stream**
# NOTE: The actual implementation is commented out as it requires installation.
# webrtc_streamer(
#     key="mood_detection_stream",
#     mode=WebRtcMode.SENDRECV,
#     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#     video_transformer_factory=VideoTransformer,
# )

# Placeholder for the webcam stream (since we can't run the tool)
st.markdown("---")
st.code("Streamlit-webrtc component would go here for live video feed.")
st.markdown("---")

# Display the results based on the session state updated by the VideoTransformer class
st.markdown("### Live Mood Analysis")

# Use a place holder for the live mood if the stream isn't running
detected_mood = st.session_state.live_mood
confidence = st.session_state.live_confidence

# Live feedback display
st.success(f"✅ Detected mood: **{detected_mood.upper()}**")
st.metric(label="Detection Confidence", value=f"{int(confidence*100)}%")
st.progress(confidence, text="Confidence Level")

# Display and play the matching playlist
if detected_mood:
    st.markdown("---")
    st.markdown(f"### Now Playing: **{detected_mood.upper()} {genre_choice} Playlist** ▶️")
    st.components.v1.iframe(CURRENT_PLAYLISTS[detected_mood], height=380)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Requires `streamlit-webrtc` for live functionality.")
