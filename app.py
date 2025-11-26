import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# --- 1. CONFIGURATION AND STYLING ---

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="EmoPlay", 
    page_icon="🎶", 
    layout="wide", # Use wide layout for better visual space
    initial_sidebar_state="collapsed"
)

# Map emotions to colors for dynamic styling and better visualization
EMOTION_COLORS = {
    "happy": "#4CAF50",    # Green
    "sad": "#2196F3",      # Blue
    "angry": "#F44336",    # Red
    "neutral": "#607D8B",  # Slate/Neutral
    "surprise": "#FFEB3B", # Yellow
    "fear": "#9C27B0",     # Purple
    "disgust": "#009688",  # Teal
}

# Real-ish Spotify Embed Links (You MUST replace these with real embed links!)
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfP7KCr5",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX1s9ktLM58Jb",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DXbe7e4W0eO07",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO"
}

# Custom CSS for a clean, dark, and modern look
st.markdown(
    """
    <style>
    /* Main Background */
    .stApp {
        background-color: #1a1a2e; /* Deep purple/blue dark background */
        color: #ffffff;
    }
    /* Header Style */
    .header-style {
        color: #ff9900; /* Bright orange accent */
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Custom container styling for results */
    .result-box {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        margin-top: 20px;
        text-align: center;
    }
    /* Specific styling for the dominant emotion */
    .dominant-emotion {
        font-size: 2.5em;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    /* Progress bar styling (customize the color dynamically) */
    .stProgress > div > div > div > div {
        background-color: var(--dominant-color, #ffffff);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 2. MAIN APPLICATION UI LAYOUT ---

st.markdown('<p class="header-style">🎶 EmoPlay – AI Music Companion 🎶</p>', unsafe_allow_html=True)
st.markdown("---")

st.markdown(
    '<p style="text-align: center; font-size: 1.1em; color: #aaaaaa;">'
    'Use your webcam to capture your current emotion. Our AI will analyze your facial expression and curate the perfect soundtrack.'
    '</p>',
    unsafe_allow_html=True,
)

# Use columns to center the camera input in the wide layout
col_spacer1, col_camera, col_spacer2 = st.columns([1, 2, 1])

with col_camera:
    img_file_buffer = st.camera_input("Capture Your Emotion")

st.markdown("---")

# --- 3. PROCESSING AND DISPLAY ---

if img_file_buffer is not None:
    
    # Initialize defaults
    emotion = "neutral" 
    sorted_scores = []
    emotion_scores = {}

    with st.spinner("🧠 Analyzing facial expressions... This takes a moment."):
        
        # Image Decoding
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if cv2_img is None:
            st.error("❌ Could not decode image from camera. Please try again.")
        else:
            try:
                # DeepFace analysis
                result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                
                # Robust result extraction
                analysis = result[0] if isinstance(result, list) and len(result) > 0 else (result if isinstance(result, dict) else None)

                if analysis and 'dominant_emotion' in analysis and 'emotion' in analysis:
                    emotion = analysis['dominant_emotion']
                    emotion_scores = analysis['emotion']
                    
                    # Sort scores for confidence meter
                    sorted_scores = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
                
            except Exception as e:
                st.warning(f"⚠️ AI couldn't detect a face clearly. Defaulting to Neutral. Error: {e}")
                emotion = "neutral"
                
    
    # --- RESULT DISPLAY (Awesome Looking UI) ---

    # Determine dominant color for dynamic styling
    detected_color = EMOTION_COLORS.get(emotion, "#607D8B")
    dominant_score = emotion_scores.get(emotion, 0) if emotion != 'neutral' else 0

    # Set the CSS variable dynamically for the progress bar color
    st.markdown(
        f'<style>:root {{--dominant-color: {detected_color};}}</style>', 
        unsafe_allow_html=True
    )

    # Use columns to separate the Confidence Meter and the Spotify Player
    col_analysis, col_player = st.columns([1, 1], gap="large")

    with col_analysis:
        
        st.markdown(
            f'<div class="result-box" style="border: 3px solid {detected_color}; background-color: {detected_color}33;">'
            f'<p style="color: {detected_color}; font-size: 1.2em; font-weight: 500;">Detected Mood</p>'
            f'<p class="dominant-emotion" style="color: {detected_color};">{emotion.upper()}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.subheader("Confidence Meter")
        st.caption("Model's certainty for the prediction:")
        
        # Display top 3 confidence scores
        for emo, score in sorted_scores[:3]:
            score_percent = f"{score:.2f}%"
            
            # Use columns for alignment
            col_emo, col_score, col_bar = st.columns([2, 1, 4])
            
            with col_emo:
                # Use color coding for emotion label
                st.markdown(f'<p style="color: {EMOTION_COLORS.get(emo, "#607D8B")}; margin: 0; padding-top: 5px;">{emo.capitalize()}</p>', unsafe_allow_html=True)
            with col_score:
                st.markdown(f'<p style="margin: 0; padding-top: 5px; font-weight: bold;">{score_percent}</p>', unsafe_allow_html=True)
            with col_bar:
                # Display individual progress bars (Note: Streamlit progress bars will use the default color if not heavily styled with CSS)
                st.progress(score / 100)
                

    with col_player:
        
        # Music Player Container
        st.markdown(
            f'<div class="result-box" style="border: 3px solid #ff9900; background-color: #ff990022; height: 100%;">'
            f'<h4 style="color: #ff9900; margin-top: 0.5rem;">🎧 Your Mood Soundtrack</h4>',
            unsafe_allow_html=True
        )
        
        spotify_url = playlists.get(emotion, playlists["neutral"])
        st.components.v1.iframe(spotify_url, height=380)

        st.markdown("</div>", unsafe_allow_html=True) # Close the music player container

else:
    col_info_spacer1, col_info, col_info_spacer2 = st.columns([1, 2, 1])
    with col_info:
        st.info("Awaiting input... Click the button above to capture your photo and start the analysis.", icon="📸") now the ui is good but not so much make it nice good looking asthetic 
