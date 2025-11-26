# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025
import streamlit as st
import random
# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoBeats - Music for Your Mood (Bollywood Edition)",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# Spotify playlist mapping for International Hits (Original Placeholders)
INT_PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",  # Sad Songs
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",  # Rock/Intense
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",  # Chill Vibes
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",  # Energetic
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",  # Dark/Spooky
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"   # Heavy
}
# **NEW FEATURE: Bollywood Playlist Mapping (Simulated/Placeholder Links)**
BOLLYWOOD_PLAYLISTS = {
    "happy":    "http://googleusercontent.com/spotify.com/bollywood_happy",    # Example: Balam Pichkari, Badtameez Dil
    "sad":      "http://googleusercontent.com/spotify.com/bollywood_sad",      # Example: Channa Mereya, Tujhe Bhula Diya
    "angry":    "http://googleusercontent.com/spotify.com/bollywood_angry",    # Example: Aarambh Hai Prachand, Sadda Haq
    "neutral":  "http://googleusercontent.com/spotify.com/bollywood_chill",    # Example: Khwabon Ke Parindey, Dil Chahta Hai
    "surprise": "http://googleusercontent.com/spotify.com/bollywood_energetic",# Example: Gallan Goodiyaan, Kar Gayi Chull
    "fear":     "http://googleusercontent.com/spotify.com/bollywood_dark",     # Example: Gali Gali, Raat Ka Nasha
    "disgust":  "http://googleusercontent.com/spotify.com/bollywood_heavy"     # Example: Emotional/Heavy songs like angry/sad
}
# --- SIMULATED COMPUTER VISION ANALYSIS (Same as before) ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection and confidence."""
    mask_present = random.random() < 0.2
    mood = random.choice(list(INT_PLAYLISTS.keys()))
    confidence = round(random.uniform(0.60, 0.99), 2)
    return mood, confidence, mask_present
# --- END SIMULATION ---
# --- APP LAYOUT ---
st.title("EmoBeats 🎶")
st.markdown("### Let your face choose the music")
# **NEW FEATURE: Genre Selection Radio Button**
genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1 # Default to Bollywood as requested
)
# Set the current playlist dictionary based on choice
CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS
st.write("Take a selfie or select your current mood — matching playlist starts instantly.")
# Camera input
img_file = st.camera_input("📸 Take a selfie for automatic mood detection")
mood = None # Initialize mood variable
if img_file:
    # Display captured image
    st.image(img_file, use_column_width=True)
    
    # Run the simulated analysis
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file)
    if mask_present:
        st.warning(
            "⚠️ **Mask Detected!** Emotion detection may be unreliable. "
            "Please remove your mask for accurate analysis or select your mood manually."
        )
        # Manual selection still uses the dictionary keys
        mood = st.selectbox("How are you feeling right now?", options=list(CURRENT_PLAYLISTS.keys()), index=3)
        st.info("Using manually selected mood.")
    else:
        # Mood detected successfully
        mood = detected_mood
        st.success(f"✅ Detected mood: **{mood.upper()}**")
        
        # Confidence Level Meter
        st.metric(label="Detection Confidence", value=f"{int(confidence*100)}%")
        st.progress(confidence, text="Confidence Level")
else:
    st.info("Or select your mood manually below")
    # Manual mood selection is the fallback
    mood = st.selectbox("How are you feeling right now?", options=list(CURRENT_PLAYLISTS.keys()), index=3)
# Display and play the matching playlist
if mood:
    st.markdown("---")
    st.markdown(f"### Now Playing: **{mood.upper()} {genre_choice} Playlist** ▶️")
    # Use the selected playlist based on the genre choice
    st.components.v1.iframe(CURRENT_PLAYLISTS[mood], height=380)
# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Full ML + Live Webcam version available on Google Colab")  
