import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# --- 1. CONFIGURATION AND STYLING ---

# Set up the Streamlit page configuration
st.set_page_config(page_title="EmoPlay", page_icon="🎵", layout="centered")

# Map emotions to colors for better UI
EMOTION_COLORS = {
    "happy": "#28a745",    # Green
    "sad": "#007bff",      # Blue
    "angry": "#dc3545",    # Red
    "neutral": "#6c757d",  # Gray
    "surprise": "#ffc107", # Yellow
    "fear": "#343a40",     # Dark Gray/Black
    "disgust": "#20c997",  # Teal
}

# Real-ish Spotify Embed Links (You should replace these with your actual links)
# IMPORTANT: These are placeholders. They should be real Spotify embed URLs.
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfP7KCr5",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX1s9ktLM58Jb",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DXbe7e4W0eO07",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO"
}

# Optional: Custom CSS for a dark theme look
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50; /* Green for progress bars */
    }
    </style>
    """, unsafe_allow_html=True)


# --- 2. MAIN APPLICATION LOGIC ---

st.title("🎵 EmoPlay – AI Music Companion")
st.info("Snap a photo, and AI will detect your mood to play the perfect track.")

# Camera Input
img_file_buffer = st.camera_input("Capture your emotion")

if img_file_buffer is not None:
    # Use a placeholder while loading
    analysis_placeholder = st.empty()

    with st.spinner("Analyzing your facial expressions..."):
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        emotion = "neutral" # Default fallback
        sorted_scores = []
        
        if cv2_img is None:
            st.error("Could not decode image from camera.")
        else:
            try:
                # DeepFace analysis
                result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                
                # Standardize result extraction (handling list or dict)
                if isinstance(result, list) and len(result) > 0:
                    analysis = result[0]
                elif isinstance(result, dict):
                    analysis = result
                else:
                    analysis = None

                if analysis and 'dominant_emotion' in analysis and 'emotion' in analysis:
                    emotion = analysis['dominant_emotion']
                    emotion_scores = analysis['emotion']
                    
                    # Sort the emotions by score (descending)
                    sorted_scores = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
                
            except Exception as e:
                st.warning(f"AI couldn't detect a face clearly. Defaulting to Neutral. Error: {e}")
                emotion = "neutral"

    # Clear the spinner placeholder after analysis is done
    analysis_placeholder.empty() 

    
    # --- 3. CONFIDENCE METER (Feature 1) ---
    
    # Get the score of the dominant emotion for the progress bar
    dominant_score = emotion_scores.get(emotion, 0) if emotion != 'neutral' else 0
    
    st.markdown(f"### 🎯 Detected Mood: **{emotion.upper()}**")
    
    # Display the confidence level for the dominant emotion
    st.progress(dominant_score / 100, text=f"Confidence: {dominant_score:.2f}%")

    st.write("Top Predicted Emotions:")
    
    # Display top 3 scores
    for i, (emo, score) in enumerate(sorted_scores[:3]):
        score_percent = f"{score:.2f}%"
        
        col_a, col_b = st.columns([1, 4])
        with col_a:
            st.write(f"**{emo.capitalize()}**")
        with col_b:
            st.caption(score_percent)


    # --- 4. SPOTIFY PLAYER (Feature 2) ---

    detected_color = EMOTION_COLORS.get(emotion, "#6c757d")

    # Use a container with border for a clean music player look
    with st.container(border=True):
        st.markdown(
            f"""
            <h3 style='color: {detected_color}; text-align: center; margin-top: 0.5rem;'>
                🎶 PERFECT SONGS FOR YOUR MOOD
            </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Display the iframe below the heading
        spotify_url = playlists.get(emotion, playlists["neutral"])
        st.components.v1.iframe(spotify_url, height=380)

else:
    st.warning("Waiting for camera input...")
