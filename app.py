# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import streamlit.components.v1 as components
from deepface import DeepFace
import cv2
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoBeats - Music for Your Mood",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PLAYLIST CONFIGURATION (Unchanged) ---
# NOTE: These are real Spotify Embed links. 
# To get these, go to Spotify > Share > Embed Playlist > Copy the 'src' URL.

INT_PLAYLISTS = {
    "happy":     "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC", # Happy Hits
    "sad":       "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1", # Sad Songs
    "angry":     "https://open.spotify.com/embed/playlist/37i9dQZF1EIeCX1SSo6M9y", # Rock/Intense
    "neutral":   "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6", # Chill Vibes
    "surprise":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM", # Energetic
    "fear":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1", # Spooky
    "disgust":   "https://open.spotify.com/embed/playlist/37i9dQZF1DX186v583rmzp"  # Heavy Metal
}

BOLLYWOOD_PLAYLISTS = {
    "happy":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM", # Bollywood Dance
    "sad":       "https://open.spotify.com/embed/playlist/37i9dQZF1DXca8AM0c05a1", # Bollywood Sad
    "angry":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX7sI57iHQdM6", # Workout/Power
    "neutral":   "https://open.spotify.com/embed/playlist/37i9dQZF1DXd8cOUiya1cg", # Bollywood Acoustic
    "surprise":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM", # Party
    "fear":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1", # Horror themes
    "disgust":   "https://open.spotify.com/embed/playlist/37i9dQZF1DX186v583rmzp"  # Heavy
}

# --- REAL DEEPFACE COMPUTER VISION ANALYSIS ---
@st.cache_resource
def load_deepface_models():
    """Load the necessary DeepFace models just once."""
    st.write("Loading DeepFace models...")
    # DeepFace models are loaded automatically when analyze() is called for the first time
    # We use a dummy call to ensure models are cached.
    # We will let the analyze function handle the loading, but keep the function for future caching optimization.
    return True

load_deepface_models()

def analyze_image_for_cv_features(image_file):
    """Analyze the image using DeepFace for emotion detection."""
    
    # 1. Convert Streamlit UploadedFile to a format DeepFace can use (numpy array)
    # Read image as bytes, then convert to a numpy array, then to OpenCV format.
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img_cv2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    try:
        # 2. Run DeepFace Analysis
        # actions=['emotion'] tells DeepFace to only analyze emotion, making it faster.
        analysis_result = DeepFace.analyze(
            img_path=img_cv2, 
            actions=['emotion'], 
            enforce_detection=True
        )
        
        # DeepFace returns a list of dictionaries for each detected face. We take the first one.
        result = analysis_result[0]
        
        # Get the dominant mood
        mood = result['dominant_emotion']
        
        # Get the confidence score for the dominant mood
        confidence = result['emotion'][mood] / 100.0 # DeepFace returns percentage, convert to float [0.0, 1.0]

        # For a real mask detection, you'd need another model or logic.
        # DeepFace detection usually fails if a mask covers the face significantly.
        # For simplicity, we assume no mask if DeepFace successfully detects a face.
        mask_present = False 

        return mood, round(confidence, 2), mask_present
        
    except Exception as e:
        # This usually happens if no face is detected (e.g., face is covered by a mask, 
        # person is looking away, or the image is poor quality).
        st.error(f"❌ Face Detection Failed: {e}")
        st.info("No face detected. Please ensure your face is clearly visible or select your mood manually.")
        return None, 0.0, True # Treat failure as a mask/failure scenario

# --- APP LAYOUT (Mostly Unchanged) ---
st.title("EmoBeats 🎶")
st.markdown("### Let your face choose the music")

# Genre Selection
genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1 
)

# Set the current playlist dictionary
CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

st.write("Take a selfie or select your current mood — matching playlist starts instantly.")

# Camera input
img_file = st.camera_input("📸 Take a selfie for automatic mood detection")

mood = None # Initialize mood variable

# --- LOGIC FLOW ---
if img_file:
    # 1. Run DeepFace Analysis
    detected_mood, confidence, analysis_failed = analyze_image_for_cv_features(img_file)
    
    # 2. Check if Analysis Failed (e.g., no face detected)
    if detected_mood is None or analysis_failed:
        # Fallback to manual selection
        st.warning("⚠️ Automatic detection failed or face not clear.")
        st.info("Please select your mood manually below.")
        mood = st.selectbox("How are you feeling?", options=list(CURRENT_PLAYLISTS.keys()))
    else:
        # 3. Success Case
        mood = detected_mood
        st.success(f"✅ Detected mood: **{mood.upper()}**")
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Confidence", value=f"{int(confidence*100)}%")
        with col2:
            st.metric(label="Genre", value=genre_choice)
            
        st.progress(confidence, text="AI Confidence Level")

else:
    # 4. No Camera Input (Default State)
    st.info("Or select your mood manually below")
    mood = st.selectbox("How are you feeling?", options=list(CURRENT_PLAYLISTS.keys()), index=0)

# --- MUSIC PLAYER ---
if mood and mood in CURRENT_PLAYLISTS:
    st.markdown("---")
    # Ensure mood is in the supported list (DeepFace sometimes outputs 'contempt', which isn't in your playlist dict)
    display_mood = mood if mood in CURRENT_PLAYLISTS else "neutral"
    
    st.subheader(f"Now Playing: **{display_mood.title()} ({genre_choice})**")
    
    # Embed Spotify Player
    playlist_url = CURRENT_PLAYLISTS[display_mood]
    components.iframe(playlist_url, height=400)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Emotion AI Prototype with DeepFace")
