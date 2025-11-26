# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import random
import streamlit.components.v1 as components

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoBeats - Music for Your Mood",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PLAYLIST CONFIGURATION ---
# NOTE: These are real Spotify Embed links. 
# To get these, go to Spotify > Share > Embed Playlist > Copy the 'src' URL.

INT_PLAYLISTS = {
    # Happy Hits (Upbeat pop/dance)
    "happy":     "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC", 
    # Sad Songs (Emotional ballads)
    "sad":       "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1", 
    # Rock Hard (Intense Rock/Angry)
    "angry":     "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U", 
    # Chill Hits (Relaxed/Neutral)
    "neutral":   "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6", 
    # Party Hits (High energy/Surprise)
    "surprise":  "https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif", 
    # Halloween/Spooky (Fear/Thriller scores)
    "fear":      "https://open.spotify.com/playlist/37i9dQZF1DX9CA7RM5s5iU", 
    # Kickass Metal (Disgust/Heavy Metal)
    "disgust":   "https://open.spotify.com/playlist/37i9dQZF1DWTcqUzwhNmKv"  
}

BOLLYWOOD_PLAYLISTS = {
    # Bollywood Dance Music (Happy/Upbeat)
    "happy":     "https://open.spotify.com/playlist/37i9dQZF1DX5q67ZpWyRrZ", 
    # Bollywood Sad Songs (Emotional)
    "sad":       "https://open.spotify.com/playlist/37i9dQZF1DX4dyrS73D35R", 
    # Gym Bollywood (High Power/Angry)
    "angry":     "https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy", 
    # Bollywood Acoustic (Calm/Neutral)
    "neutral":   "https://open.spotify.com/playlist/37i9dQZF1DX6GjY5TqYjXN", 
    # Punjabi 101 (High Energy/Party)
    "surprise":  "https://open.spotify.com/playlist/37i9dQZF1DX5cZuAHLNjGz", 
    # Suspense/Thriller BGM (Fear)
    "fear":      "https://open.spotify.com/playlist/37i9dQZF1DX1RxZbd13t8s", 
    # Desi Hip Hop/Hard Hitting (Aggressive/Heavy)
    "disgust":   "https://open.spotify.com/playlist/37i9dQZF1DWSYIVP8d447O"  
}

# --- SIMULATED COMPUTER VISION ANALYSIS ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection and confidence."""
    # In a real app, you would pass 'image_file' to a model like DeepFace or Fer2013
    mask_present = random.random() < 0.15 # 15% chance of mask
    mood = random.choice(list(INT_PLAYLISTS.keys()))
    confidence = round(random.uniform(0.60, 0.99), 2)
    return mood, confidence, mask_present

# --- APP LAYOUT ---
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
    # 1. Run Simulation
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file)
    
    # 2. Check for Mask
    if mask_present:
        st.warning("⚠️ **Mask Detected!** Analysis unreliable.")
        st.info("Please select your mood manually below.")
        # Fallback to manual
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
if mood:
    st.markdown("---")
    st.subheader(f"Now Playing: **{mood.title()} ({genre_choice})**")
    
    # Embed Spotify Player
    playlist_url = CURRENT_PLAYLISTS[mood]
    components.iframe(playlist_url, height=400)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Emotion AI Prototype")
