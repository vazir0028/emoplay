import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# 1. Page Config
st.set_page_config(page_title="EmoPlay", page_icon="🎵", layout="centered")

# 2. CSS for styling (Optional: Makes it look more 'Pro')
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 EmoPlay – AI Music Companion")
st.write("Snap a photo, and AI will detect your mood to play the perfect track.")

# 3. Real Spotify Embed Links (Use 'embed' in the URL)
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",    # Sad Songs
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfP7KCr5",  # Rage Beats
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M",# Chill/Focus
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX1s9ktLM58Jb", # Hype
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DXbe7e4W0eO07",   # Calm Down
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO" # Confidence/Attitude
}

# 4. Camera Input
img_file_buffer = st.camera_input("Capture your emotion")

if img_file_buffer is not None:
    # 5. Loading Spinner (Crucial for UX while DeepFace processes)
    with st.spinner("Analyzing your facial expressions..."):
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        emotion = "neutral" # Default fallback
        
        if cv2_img is None:
            st.error("Could not decode image.")
        else:
            try:
                # Enforce detection=False prevents crash if face isn't perfectly clear
                result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                
                # Logic to handle different DeepFace versions
                if isinstance(result, list) and len(result) > 0:
                    emotion = result[0].get('dominant_emotion')
                elif isinstance(result, dict):
                    emotion = result.get('dominant_emotion')
                
                # Fallback if dictionary extraction fails
                if not emotion:
                    emotion = 'neutral'
                    
            except Exception as e:
                st.warning(f"AI couldn't detect a face clearly. Defaulting to Neutral. ({e})")
                emotion = "neutral"

    # 6. Display Results
    st.markdown(f"### 😲 Detected Mood: **{emotion.upper()}**")
    
    # Get the URL, default to neutral if emotion key is missing
    spotify_url = playlists.get(emotion, playlists["neutral"])
    
    st.components.v1.iframe(spotify_url, height=380)

else:
    st.info("Waiting for input... Please take a picture to start.")
