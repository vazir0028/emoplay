import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Emotion Music Player", page_icon="🎵", layout="wide")

# --- HIDE TENSORFLOW WARNINGS ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- TITLE & SIDEBAR ---
st.title("🎵 Emotion-Based Music Recommender")
st.write("Take a selfie, and I'll play music that matches your mood!")

st.sidebar.header("🔑 Setup Keys")
st.sidebar.info("Get these from the Spotify Developer Dashboard.")
client_id = st.sidebar.text_input("Spotify Client ID", type="password")
client_secret = st.sidebar.text_input("Spotify Client Secret", type="password")

# --- FUNCTIONS ---

@st.cache_resource
def get_spotify_client(c_id, c_secret):
    try:
        auth_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp
    except Exception as e:
        return None

def get_mood_playlist_query(emotion):
    # Mapping emotions to search terms
    mood_mapping = {
        "angry": "calm classical piano",
        "disgust": "heavy metal",
        "fear": "comforting acoustic",
        "happy": "top hits upbeat",
        "sad": "uplifting pop",
        "surprise": "electronic dance",
        "neutral": "lofi study beats"
    }
    return mood_mapping.get(emotion, "pop music")

# --- MAIN APP LOGIC ---

# 1. Check if keys are entered
if not client_id or not client_secret:
    st.warning("⚠️ Please enter your Spotify API Keys in the sidebar to start.")
else:
    sp = get_spotify_client(client_id, client_secret)

    # 2. Camera Input
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Your Photo")
        img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # Convert the buffer to an image that DeepFace can read
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # 3. Analyze Emotion
        with col2:
            st.subheader("🧠 Analysis Results")
            with st.spinner("Analyzing your face..."):
                try:
                    # DeepFace analysis
                    result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                    
                    # Handle list vs dict return type
                    if isinstance(result, list):
                        result = result[0]
                    
                    dominant_emotion = result['dominant_emotion']
                    
                    st.success(f"Detected Mood: **{dominant_emotion.upper()}**")
                    
                    # 4. Search Spotify
                    search_query = get_mood_playlist_query(dominant_emotion)
                    st.write(f"🎶 Searching for: *{search_query}*")
                    
                    search_results = sp.search(q=search_query, type='playlist', limit=1)
                    
                    if search_results['playlists']['items']:
                        playlist = search_results['playlists']['items'][0]
                        playlist_name = playlist['name']
                        playlist_id = playlist['id']
                        
                        st.markdown(f"### 🎧 Playing: {playlist_name}")
                        
                        # 5. Embed Player
                        # We use HTML iframe to embed the Spotify player
                        spotify_embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
                        components_html = f"""
                        <iframe style="border-radius:12px" src="{spotify_embed_url}" 
                        width="100%" height="352" frameBorder="0" 
                        allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                        loading="lazy"></iframe>
                        """
                        st.components.v1.html(components_html, height=360)
                        
                    else:
                        st.error("No playlists found for this mood.")

                except Exception as e:
                    st.error(f"Error processing image: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("B.Tech Project | Built with Streamlit & DeepFace")
