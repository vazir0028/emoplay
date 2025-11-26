# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import random
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EmoBeats | AI Music Player",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR "AWESOME" UI ---
st.markdown("""
    <style>
         1. MAIN BACKGROUND: Deep Gradient 
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            background-attachment: fixed;
            color: white;
        }
        
        2. TITLE STYLING */
        .title-text {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 800;
            font-size: 3.5rem;
            background: -webkit-linear-gradient(eee, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0px;
        }
        .subtitle-text {
            text-align: center;
            color: #b3b3b3;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }

         3. GLASSMORPHISM CARDS */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        4. RADIO BUTTON STYLING (Pill Shape) 
        div[role="radiogroup"] {
            background: rgba(255, 255, 255, 0.1);
            padding: 5px;
            border-radius: 15px;
            display: flex;
            justify-content: center;
        }
        div[data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem;
        }

        5. METRIC CARDS 
        div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            color: #00d4ff !important;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        div[data-testid="stMetricLabel"] {
            color: #e0e0e0 !important;
        }

        /* 6. CAMERA INPUT BORDER */
        div[data-testid="stCameraInput"] {
            border: 2px solid #00d4ff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        }

         7. ANIMATION FOR MUSIC PLAYER 
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 212, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0); }
        }
        .music-container {
            animation: pulse 2s infinite;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# --- PLAYLIST CONFIGURATION (UPDATED AGGRESSIVE LISTS) ---
INT_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1EIeCX1SSo6M9y",
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM",
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX186v583rmzp"
}

BOLLYWOOD_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DXca8AM0c05a1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DX7sI57iHQdM6", # High Energy Workout
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DXd8cOUiya1cg",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUfTFmNBRM",
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX9tPFwDMOaN1",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWTq0vE13F9XQ"  # Punjabi X (Heavy/Loud)
}

# --- LOGIC ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection."""
    mask_present = random.random() < 0.15 
    mood = random.choice(list(INT_PLAYLISTS.keys()))
    confidence = round(random.uniform(0.60, 0.99), 2)
    return mood, confidence, mask_present

# --- APP LAYOUT ---

# Custom Title
st.markdown('<h1 class="title-text">EmoBeats 🎧</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">AI-Powered Emotion Music Player</p>', unsafe_allow_html=True)

# Main Control Panel (Glass Card)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
genre_choice = st.radio(
    "Select Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1
)
st.markdown('</div>', unsafe_allow_html=True)

CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

# Camera Section
st.write("📸 **Scan your mood:**")
img_file = st.camera_input("camera", label_visibility="collapsed")

mood = None

# --- RESULTS SECTION ---
if img_file:
    # Analysis
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if mask_present:
        st.warning("⚠️ **Face Mask Detected!**")
        st.write("Detection might be inaccurate. Select manually:")
        mood = st.selectbox("Current Mood", options=list(CURRENT_PLAYLISTS.keys()))
    else:
        mood = detected_mood
        
        # Layout for metrics
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.metric("Mood Detected", f"{mood.upper()}")
        with c2:
            st.metric("Confidence", f"{int(confidence*100)}%")
        with c3:
            st.metric("Playlist", genre_choice)
            
        st.success(f"Playing **{mood.upper()}** tracks for you!")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Default Manual Selector
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.info("Waiting for camera... or select manually below:")
    mood = st.selectbox("Manual Selection", options=list(CURRENT_PLAYLISTS.keys()), index=0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- MUSIC PLAYER (Pulsing Effect) ---
if mood:
    st.markdown("---")
    st.markdown(f"### 🎵 Now Playing: {mood.title()} Mix")
    
    playlist_url = CURRENT_PLAYLISTS[mood]
    
    # Wrap iframe in a div for animation
    st.markdown('<div class="music-container">', unsafe_allow_html=True)
    components.iframe(playlist_url, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #888;">
        <small>Built with ❤️ by <b>Vazir</b> | B.Tech CSE 2025</small>
    </div>
""", unsafe_allow_html=True)
