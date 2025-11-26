import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image

# 1. Set Page Configuration
st.set_page_config(page_title="Emotion Music Recommender", page_icon="🎵")

st.title("🎵 Emotion Based Music Recommendation")
st.write("This app uses DeepFace to detect your emotion and recommend music.")

# 2. Camera Input
# Streamlit has a built-in camera input widget that is easier to use in Cloud than cv2.VideoCapture
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # Convert the file to an opencv image.
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Display processing message
    with st.spinner('Analyzing emotion... (This might take a moment)'):
        try:
            # 3. Analyze Emotion
            # enforce_detection=False prevents crash if face isn't perfect
            result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
            
            # DeepFace returns a list of dictionaries in newer versions
            if isinstance(result, list):
                result = result[0]
            
            dominant_emotion = result['dominant_emotion']
            
            st.success(f"Detected Emotion: **{dominant_emotion.upper()}**")
            
            # 4. Logic for Spotify (Placeholder)
            st.subheader(f"Recommended Playlist for {dominant_emotion}:")
            if dominant_emotion == 'happy':
                st.write("🎶 Playing 'Happy Hits'...")
                # Add your Spotify logic here
            elif dominant_emotion == 'sad':
                st.write("🎶 Playing 'Melancholy Mix'...")
            else:
                st.write(f"🎶 Playing {dominant_emotion} vibes...")

        except Exception as e:
            st.error(f"Error analyzing face: {e}")
            st.info("Please make sure your face is clearly visible.")
