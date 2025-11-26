import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np
import spotipy # New Import
from spotipy.oauth2 import SpotifyClientCredentials # New Import

# --- 1. CONFIGURATION AND STYLING ---
# (Keep your existing st.set_page_config and CSS setup here)
# ...

# --- NEW: SPOTIFY EMOTION MAPPING TO AUDIO FEATURES ---

# Map DeepFace emotions to Spotify's Audio Feature values (0.0 to 1.0)
# 'Valence' is musical positivity (happy sounds = high valence)
# 'Energy' is intensity and activity (angry/happy = high energy)
# 'Danceability' is suitability for dancing (happy/surprise = high danceability)

EMOTION_FEATURE_MAP = {
    "happy": {"target_valence": 0.85, "target_energy": 0.8, "target_danceability": 0.75, "min_popularity": 50},
    "sad": {"target_valence": 0.25, "target_energy": 0.3, "target_acousticness": 0.7, "min_popularity": 40},
    "angry": {"target_valence": 0.4, "target_energy": 0.9, "target_tempo": 140, "min_popularity": 50}, # High energy, moderate valence
    "neutral": {"target_valence": 0.5, "target_energy": 0.5, "target_acousticness": 0.5, "min_popularity": 50},
    "surprise": {"target_valence": 0.7, "target_energy": 0.7, "target_danceability": 0.8, "min_popularity": 60},
    "fear": {"target_valence": 0.3, "target_energy": 0.6, "target_tempo": 100, "min_popularity": 40}, # Low valence, moderate energy
    "disgust": {"target_valence": 0.2, "target_energy": 0.5, "target_liveness": 0.8, "min_popularity": 30} # Low valence, focus on liveness/raw sound
}

# --- NEW: SPOTIFY API INITIALIZATION ---
# Load credentials from the secure secrets.toml file
CLIENT_ID = st.secrets["spotify"]["client_id"]
CLIENT_SECRET = st.secrets["spotify"]["client_secret"]

# Initialize Spotify client (Client Credentials Flow)
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))
except Exception as e:
    st.error(f"❌ Could not initialize Spotify. Check your secrets.toml file and network connection. Error: {e}")
    sp = None # Set to None if initialization fails

# --- NEW: FUNCTION TO GET DYNAMIC SPOTIFY EMBED URL ---

def get_dynamic_spotify_embed(emotion: str) -> str:
    """Uses Spotify API to find tracks based on audio features related to the emotion."""
    if sp is None:
        return "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M" # Fallback Neutral Playlist

    # Get feature targets for the dominant emotion
    features = EMOTION_FEATURE_MAP.get(emotion, EMOTION_FEATURE_MAP["neutral"])
    
    # Use the recommendation endpoint with audio features
    try:
        results = sp.recommendations(
            seed_genres=['pop', 'chill', 'electronic', 'rock', 'ambient'], # Broad genres
            limit=10,
            **features # Unpack the audio features (target_valence, target_energy, etc.)
        )

        track_uris = [track['uri'] for track in results.get('tracks', [])]
        
        if not track_uris:
            st.warning("⚠️ No songs found for this emotion mapping. Using fallback playlist.")
            return "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M"
            
        # Create a comma-separated list of track URIs for the embed
        # NOTE: Spotify embed URLs often work better with a specific track/playlist URI
        # For simplicity, we'll embed the first track found:
        first_track_uri = track_uris[0].split(':')[-1]
        
        # Return the embed URL for a single track
        return f"https://open.spotify.com/embed/track/{first_track_uri}?utm_source=generator"
        
    except Exception as e:
        st.error(f"Spotify API Error during recommendation: {e}. Check token and scope.")
        return "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M" # Fallback

# --- 2. MAIN APPLICATION UI LAYOUT ---
# (Keep the UI code mostly the same)
# ...

# --- 3. PROCESSING AND DISPLAY (The execution block) ---

if img_file_buffer is not None:
    # ... (Keep all your DeepFace analysis logic here - 3A) ...

    # --- 3B. RESULT DISPLAY (Awesome Looking UI) ---
    # ... (Keep all your visual setup: colors, CSS, columns) ...

    with col_player:
        st.markdown(
            f'<div class="result-box" style="border: 3px solid #FF6B6B; background-color: #FF6B6B22; height: 100%;">'
            f'<h4 style="color: #FF6B6B; margin-top: 0.5rem;">🎧 Your Mood Soundtrack (Dynamic)</h4>',
            unsafe_allow_html=True
        )
        
        # --- CRITICAL CHANGE HERE ---
        # Call the new dynamic function using the detected emotion
        spotify_url = get_dynamic_spotify_embed(emotion)
        
        # Embed the generated track/playlist
        st.components.v1.iframe(spotify_url, height=380)

        st.markdown("</div>", unsafe_allow_html=True) 

# ... (Keep the initial state 'else' block) ...
