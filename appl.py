# Camera input
# existing imports
import streamlit as st
import random

# ADD THESE 3 LINES BELOW THE ABOVE
from deepface import DeepFace
import cv2
import numpy as np


img_file = st.camera_input("Take a selfie for automatic mood detection")

if img_file:
    # Display captured image
    st.image(img_file, use_column_width=True)
    
    # ---- REAL EMOTION DETECTION STARTS HERE ----
    bytes_data = img_file.getvalue()
    img_array = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    with st.spinner("Detecting your mood..."):
        try:
            result = DeepFace.analyze(
                frame, 
                actions=['emotion'], 
                enforce_detection=False, 
                silent=True
            )
            mood = result[0]['dominant_emotion'].lower()
            confidence = result[0]['emotion'][mood.capitalize()]

            st.success(f"Detected mood: **{mood.upper()}** ({confidence:.1f}% confidence)")

            # Bonus: Show detailed emotions
            with st.expander("View all emotions"):
                emotions = result[0]['emotion']
                for emo, val in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"{emo.capitalize()}: {val:.1f}%")

        except Exception as e:
            st.error("No face detected. Try again with better lighting or closer shot!")
            mood = "neutral"
    # ---- REAL EMOTION DETECTION ENDS HERE ----

else:
    st.info("Or select your mood manually below")
    mood = st.selectbox("How are you feeling right now?", 
                        options=list(PLAYLISTS.keys()), 
                        index=3)  # default neutral
