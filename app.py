import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("EmoPlay – Music That Matches Your Mood")
st.write("Allow camera → look at webcam → songs change with your emotion!")

playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC?utm_source=generator",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1?utm_source=generator",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg?utm_source=generator",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL?utm_source=generator",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr?utm_source=generator",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned?utm_source=generator",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg?utm_source=generator"
}

img_file_buffer = st.camera_input(" ")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if cv2_img is None:
        st.error("Could not decode the image from the camera.")
        emotion = "neutral" 
    else:
        try:
            result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
            # DeepFace.analyze may return a dict (single face) or a list (multiple faces)
            if isinstance(result, list) and len(result) > 0:
                emotion = result[0].get('dominant_emotion') or result[0].get('emotion', {}).get('dominant_emotion', 'neutral')
            elif isinstance(result, dict):
                emotion = result.get('dominant_emotion') or result.get('emotion', {}).get('dominant_emotion', 'neutral')
            else:
                emotion = 'neutral'
        except Exception as e:
            st.warning(f"Emotion detection failed: {e}")
            emotion = "neutral"
    
    st.write(f"### Detected Mood → **{emotion.upper()}**")
    st.write("#### Now Playing Perfect Songs For Your Mood ↓")
    st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380)
else:
    st.write("Waiting for camera… click the camera above")
