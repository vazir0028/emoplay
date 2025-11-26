import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# --- 1. CONFIGURATION AND STYLING ---

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="EmoPlay",
    page_icon="🎧",  # Changed icon for a music focus
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Map emotions to colors and icons for dynamic styling and better visualization
EMOTION_DATA = {
    "happy": {"color": "#4CAF50", "icon": "😊"},  # Green
    "sad": {"color": "#2196F3", "icon": "😔"},    # Blue
    "angry": {"color": "#F44336", "icon": "😡"},  # Red
    "neutral": {"color": "#607D8B", "icon": "😐"}, # Slate/Neutral
    "surprise": {"color": "#FFEB3B", "icon": "😮"}, # Yellow
    "fear": {"color": "#9C27B0", "icon": "😨"},    # Purple
    "disgust": {"color": "#009688", "icon": "🤢"}, # Teal
}

# Real-ish Spotify Embed Links (You MUST replace these with real embed links!)
# NOTE: In a real app, these should point to Spotify embedded players.
playlists = {
    "happy": "https://developer.spotify.com/embed/happyspotifyplaylist",
    "sad": "https://developer.spotify.com/embed/sadspotifyplaylist",
    "angry": "https://developer.spotify.com/embed/angryspotifyplaylist",
    "neutral": "https://developer.spotify.com/embed/neutralspotifyplaylist",
    "surprise": "https://developer.spotify.com/embed/surprisespotifyplaylist",
    "fear": "https://developer.spotify.com/embed/fearspotifyplaylist",
    "disgust": "https://developer.spotify.com/embed/disgustspotifyplaylist"
}

# Custom CSS for a clean, aesthetic, and modern dark look
st.markdown(
    """
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #121212; /* Very dark, Spotify-like black */
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Style - More prominent and centered */
    .header-style {
        color: #1DB954; /* Spotify Green Accent */
        text-align: center;
        margin-bottom: 20px;
        font-size: 3em;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-shadow: 0 0 5px rgba(29, 185, 84, 0.4); /* Subtle glow */
    }

    /* Subheader/Description */
    .stMarkdown p {
        color: #b3b3b3;
    }

    /* Card/Box Styling - Introducing depth and subtle lift */
    .result-card, .info-card {
        padding: 25px;
        border-radius: 12px;
        background-color: #1E1E1E; /* Darker grey for card background */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5), 0 0 10px rgba(0, 0, 0, 0.3);
        margin-top: 15px;
        transition: transform 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-3px);
    }
    
    /* Dominant Emotion Display */
    .dominant-emotion-display {
        padding: 30px 10px;
        border-radius: 12px;
        text-align: center;
        background: linear-gradient(145deg, var(--dominant-color-light), var(--dominant-color-dark));
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.4);
    }

    .dominant-emotion-text {
        font-size: 3.5em;
        font-weight: 900;
        text-transform: uppercase;
        margin: 0;
        letter-spacing: 2px;
        color: #ffffff; /* White text on color background */
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
    }
    
    /* Custom Progress Bar Styling (Manual Implementation) */
    .progress-container {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .emotion-label {
        width: 80px;
        font-weight: 600;
        color: #e0e0e0;
    }
    .progress-bar-bg {
        flex-grow: 1;
        height: 10px;
        background-color: #333333; /* Dark track */
        border-radius: 5px;
        margin: 0 10px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }
    .score-text {
        width: 50px;
        text-align: right;
        font-weight: 700;
        color: #ffffff;
    }

    /* Streamlit components overrides for better look */
    .stButton>button {
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #1AA84E;
    }
    .stCameraInput {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to render the custom progress bar
def render_custom_progress_bar(emotion, score, color):
    score_percent = f"{score:.2f}%"
    icon = EMOTION_DATA.get(emotion, {"icon": "❓"})["icon"]
    
    # Use HTML to render the custom bar with dynamic color and width
    st.markdown(
        f"""
        <div class="progress-container">
            <span class="emotion-label" style="color: {color};">{icon} {emotion.capitalize()}</span>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {score}%; background-color: {color};"></div>
            </div>
            <span class="score-text">{score_percent}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- 2. MAIN APPLICATION UI LAYOUT ---

st.markdown('<p class="header-style">🎧 EmoPlay – AI Music Companion</p>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; font-size: 1.1em; color: #b3b3b3;">'
    'Instantly analyze your current mood via webcam and get a personalized Spotify playlist tailored to your emotion.'
    '</p>',
    unsafe_allow_html=True,
)

st.markdown("---")

# Use columns to center the camera input in the wide layout
col_spacer1, col_camera, col_spacer2 = st.columns([1, 2, 1])

with col_camera:
    # Use a more engaging subheader for the camera input
    st.markdown('<h3 style="text-align: center; color: #ffffff;">📸 Step 1: Capture Your Mood</h3>', unsafe_allow_html=True)
    img_file_buffer = st.camera_input("Capture Your Emotion")

st.markdown("---")

# --- 3. PROCESSING AND DISPLAY ---

if img_file_buffer is not None:
    
    # Initialize defaults
    emotion = "neutral"
    sorted_scores = []
    emotion_scores = {}

    with st.spinner("🧠 Analyzing facial expressions... Getting that perfect soundtrack."):
        
        # Image Decoding
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if cv2_img is None:
            st.error("❌ Could not decode image from camera. Please try again.")
        else:
            try:
                # DeepFace analysis (CRITICAL FIX: Use 'opencv' detector backend)
                result = DeepFace.analyze(
                    cv2_img, 
                    actions=['emotion'], 
                    enforce_detection=False,
                    detector_backend='opencv' # <-- FIX applied here!
                )
                
                # Robust result extraction
                analysis = result[0] if isinstance(result, list) and len(result) > 0 else (result if isinstance(result, dict) else None)

                if analysis and 'dominant_emotion' in analysis and 'emotion' in analysis:
                    emotion = analysis['dominant_emotion']
                    emotion_scores = analysis['emotion']
                    
                    # Sort scores for confidence meter
                    sorted_scores = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
                
            except Exception as e:
                # Catch DeepFace errors (e.g., no face detected)
                st.warning(f"⚠️ AI couldn't detect a face clearly or failed to analyze. Defaulting to Neutral. Error: {e}")
                emotion = "neutral"
                
    
    # --- RESULT DISPLAY (Aesthetic UI) ---

    # Determine dominant color for dynamic styling
    detected_data = EMOTION_DATA.get(emotion, EMOTION_DATA["neutral"])
    detected_color = detected_data["color"]
    detected_icon = detected_data["icon"]

    # Set the CSS variables dynamically for the progress bar color
    st.markdown(
        f'<style>:root {{--dominant-color-dark: {detected_color}; --dominant-color-light: {detected_color}AA;}}</style>',
        unsafe_allow_html=True
    )

    st.markdown('<h3 style="text-align: center; color: #ffffff;">✨ Step 2: Analysis Results</h3>', unsafe_allow_html=True)
    
    # Use columns to separate the Confidence Meter and the Spotify Player
    col_analysis, col_player = st.columns([1, 1], gap="large")

    with col_analysis:
        
        # --- Dominant Emotion Card ---
        st.markdown(
            f'<div class="dominant-emotion-display">'
            f'<p style="color: #ffffff; font-size: 1.2em; font-weight: 500; margin-bottom: 5px;">Your Mood is...</p>'
            f'<p class="dominant-emotion-text">{detected_icon} {emotion.upper()}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
        st.subheader("Confidence Meter")
        st.caption("Model's certainty across all expressions:")
        
        # Display all emotion scores using the custom progress bar function
        for emo, score in sorted_scores:
            color = EMOTION_DATA.get(emo, EMOTION_DATA["neutral"])["color"]
            render_custom_progress_bar(emo, score, color)
        
        st.markdown(f'</div>', unsafe_allow_html=True) # Close result-card
            
    with col_player:
        
        # --- Music Player Card ---
        st.markdown(
            f'<div class="result-card info-card" style="border: 2px solid #1DB954; height: 100%;">'
            f'<h3 style="color: #1DB954; margin-top: 0.5rem; text-align: center;">🎧 Your Mood Soundtrack</h3>'
            f'<p style="text-align: center;">Here is a playlist perfectly matched to your **{emotion.upper()}** mood.</p>',
            unsafe_allow_html=True
        )
        
        spotify_url = playlists.get(emotion, playlists["neutral"])
        
        # Use HTML component for the embed
        # NOTE: Using a placeholder URL. For production, ensure this is a valid Spotify embed URL.
        st.components.v1.iframe(
            f"https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M?utm_source=generator", 
            height=380, 
            scrolling=True
        )

        st.markdown("</div>", unsafe_allow_html=True) # Close the result-card

else:
    # Initial state with aesthetic info box
    col_info_spacer1, col_info, col_info_spacer2 = st.columns([1, 2, 1])
    with col_info:
        st.markdown(
            f'<div class="info-card" style="border-left: 5px solid #1DB954; text-align: center;">'
            f'<h4 style="color: #1DB954; margin-top: 0;">Welcome to EmoPlay!</h4>'
            f'<p>Click **"Capture Your Emotion"** above to take a photo. '
            f'Our AI will analyze your facial expression using DeepFace and generate a custom music experience.</p>'
            f'<p style="font-style: italic; color: #888888;">Ensure good lighting and a visible face for the best results!</p>'
            f'</div>',
            unsafe_allow_html=True
        )
