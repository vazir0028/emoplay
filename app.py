import streamlit as st

st.set_page_config(page_title="EmoPlay", layout="centered")
st.title("🎵 EmoPlay – Music That Matches Your Mood")
st.write("**Type your mood below → Get personalized Spotify playlist!** (Camera version in Colab)")

# Spotify playlists
playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

mood = st.selectbox("Select your current mood:", list(playlists.keys()))

if mood:
    st.success(f"🎭 Detected/Selected: **{mood.upper()}**")
    st.write("### 🎶 Now Playing: Songs For Your Mood")
    st.components.v1.iframe(playlists[mood], height=380, scrolling=False)

st.caption("Made by Vazir | BTech CSE | Full ML version: [Colab Link Here] | Deployed on Streamlit")
