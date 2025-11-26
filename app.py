import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# --- 1. CONFIGURATION AND STYLING (Aesthetic Overhaul) ---

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="EmoPlay", 
    page_icon="🎶", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Deep Jewel Tone Palette for Aesthetic Dark Theme
EMOTION_COLORS = {
    "happy": "#FFD700",    # Gold (Joyful)
    "sad": "#4169E1",      # Royal Blue (Depth)
    "angry": "#C41E3A",    # Scarlet Red (Intensity)
    "neutral": "#B0C4DE",  # Light Steel Blue (Calm)
    "surprise": "#3CB371", # Medium Sea Green (Vibrancy)
    "fear": "#9370DB",     # Medium Purple (Mystery)
    "disgust": "#A52A2A",  # Brown (Aversion)
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

# Custom CSS for a Deep Jewel Tone, High-Contrast Aesthetic
st.markdown(
    """
    <style>
    /* Main Background - Rich Black/Deep Navy */
    .stApp {
        background-color: #0F1626; /* Darker than before */
        color: #F0F0F0; /* Off-white text */
    }
    /* Header Style - Neon Accent */
    .header-style {
        color: #FF6B6B; /* Coral/Salmon Accent */
        text-align: center;
        margin-bottom: 25px;
        font-size: 2.8em;
        font-family: 'Georgia', serif;
        font-weight: 700;
        letter-spacing: 2px;
    }
    /* Description Text */
    .stMarkdown p {
        color: #C0C0C0; /* Soft gray for body text */
    }
    /* Result Boxes/Cards */
    .result-box {
        padding: 30px;
        border-radius: 15px; /* Softer corners */
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.1); /* Subtle glowing effect */
        margin-top: 20px;
        text-align: center;
        transition: transform 0.3s ease-in-out;
    }
    /* Dominant Emotion Header */
    .dominant-emotion {
        font-size: 3.5em; /* Larger, more impactful */
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    /* Custom Progress Bar for Confidence Meter */
    .stProgress > div > div > div {
        background-color: #333950; /* Dark track color */
        border-radius: 5px;
        height: 10px;
    }
    /* Progress Bar Fill - Uses dynamic color via Streamlit variable */
    .stProgress > div > div > div > div {
        background-color: var(--dominant-color, #ffffff);
        border-radius: 5px;
    }
    /* Remove default camera label */
    .stCameraInput label {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 2. MAIN APPLICATION UI LAYOUT ---

st.markdown('<p class="header-style">🎶 EmoPlay – AI Music Companion 🎶</p>', unsafe_allow_html=True)

st.markdown(
    '<p style="text-align: center; font-size: 1.2em;">'
    'Capture your current emotion. Our AI analyzes your expression and curates a **Perfect Mood Soundtrack**.'
    '</p>',
    unsafe_allow_html=True,
)
st.write(" ") # Spacer

# Center the camera input
col_spacer1, col_camera, col_spacer2 = st.columns([1, 2, 1])
with col_camera:
    st.markdown('<p style="text-align: center; color: #FF6B6B; font-weight: bold;">Step 1: Look into your camera and snap a photo.</p>', unsafe_allow_html=True)
    img_file_buffer = st.camera_input("Capture Your Emotion")

st.markdown("---")

# --- 3. PROCESSING AND DISPLAY ---

if img_file_buffer is not None:
    
    # Initialize defaults
    emotion = "neutral" 
    sorted_scores = []
    emotion_scores = {}

    # --- 3A. ANALYSIS ---
    analysis_container = st.container()
    with analysis_container:
        with st.spinner("🧠 Analyzing facial expressions... Please wait for the magic."):
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            if cv2_img is None:
                st.error("❌ Could not decode image. Analysis failed.")
            else:
                try:
                    result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                    
                    analysis = result[0] if isinstance(result, list) and len(result) > 0 else (result if isinstance(result, dict) else None)

                    if analysis and 'dominant_emotion' in analysis and 'emotion' in analysis:
                        emotion = analysis['dominant_emotion']
                        emotion_scores = analysis['emotion']
                        sorted_scores = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
                    
                except Exception as e:
                    st.warning(f"⚠️ Face not clearly detected. Defaulting to Neutral. ({e})")
                    emotion = "neutral"
                    
    
    # --- 3B. RESULT DISPLAY (Awesome Looking UI) ---

    detected_color = EMOTION_COLORS.get(emotion, "#B0C4DE")
    dominant_score = emotion_scores.get(emotion, 0) if emotion != 'neutral' else 0

    # Apply dynamic CSS variable for progress bar fill color
    st.markdown(
        f'<style>:root {{--dominant-color: {detected_color};}}</style>', 
        unsafe_allow_html=True
    )

    # Use columns to separate the Confidence Meter and the Spotify Player
    col_analysis, col_player = st.columns([1, 1], gap="large")

    with col_analysis:
        
        # Dominant Emotion Card (Dynamic Color Border)
        st.markdown(
            f'<div class="result-box" style="border: 3px solid {detected_color}; background-color: {detected_color}22;">'
            f'<p style="color: #F0F0F0; font-size: 1.2em; font-weight: 500;">Your AI-Detected Mood Is:</p>'
            f'<p class="dominant-emotion" style="color: {detected_color};">{emotion.upper()}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.subheader("Confidence Breakdown")
        st.caption("The model's internal certainty across emotional classes:")
        st.write("") # Spacer
        
        # Confidence Meter Display
        for emo, score in sorted_scores[:4]: # Show top 4 emotions
            score_percent = f"{score:.2f}%"
            
            # Use columns for sleek label/bar alignment
            col_emo, col_bar = st.columns([3, 5])
            
            # Label with color accent
            with col_emo:
                st.markdown(f'<p style="color: {EMOTION_COLORS.get(emo, "#B0C4DE")}; margin: 0; padding-top: 5px; font-weight: 600;">{emo.capitalize()}</p>', unsafe_allow_html=True)
            
            # Bar with percentage text overlay (using standard Streamlit progress)
            with col_bar:
                # *** CRITICAL FIX: Explicitly convert to float to prevent StreamlitAPIException ***
                st.progress(float(score) / 100, text=score_percent)
                

    with col_player:
        
        # Music Player Card (Fixed Accent Color Border)
        st.markdown(
            f'<div class="result-box" style="border: 3px solid #FF6B6B; background-color: #FF6B6B22; height: 100%;">'
            f'<h4 style="color: #FF6B6B; margin-top: 0.5rem;">🎧 Your Mood Soundtrack</h4>',
            unsafe_allow_html=True
        )
        
        spotify_url = playlists.get(emotion, playlists["neutral"])
        st.components.v1.iframe(spotify_url, height=380)

        st.markdown("</div>", unsafe_allow_html=True) 

else:
    # Initial state with aesthetic call to action
    col_info_spacer1, col_info, col_info_spacer2 = st.columns([1, 2, 1])
    with col_info:
        st.markdown(
            '<div style="background-color: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #333950; text-align: center;">'
            '<p style="color: #FFD700; font-size: 1.5em; margin-bottom: 0;">Ready to find your vibe?</p>'
            '<p style="color: #B0C4DE;">Click **"Capture Your Emotion"** above to begin the facial analysis.</p>'
            '</div>',
            unsafe_allow_html=True
        ) is this model can i use it btech projet 
