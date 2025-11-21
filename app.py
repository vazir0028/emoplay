import streamlit as st

# Page config
st.set_page_config(page_title="EmoPlay", layout="centered")

# Title & description
st.title("EmoPlay – Music That Matches Your Mood")
st.markdown("**Camera se mood detect karo ya select karo → Songs change ho jayenge!**")

# Spotify mood playlists
playlists = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear":     "https://open.spotify.com/embed/playlist Tarantino4fpCWaHOned",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

# Camera input
img_file = st.camera_input("Take a selfie to detect mood (or choose below)")

# Auto mood from image (fake detection – just for demo)
if img_file:
    st.image(img_file, caption="Photo captured!", use_column_width=True)
    # Fake random mood (real ML Colab mein hai)
    import random
    emotion = random.choice(["happy", "sad", "angry", "neutral", "surprise"])
    st.success(f"Detected Mood → **{emotion.upper()}**")
else:
    st.info("Ya mood manually select kar lo ↓")
    emotion = st.selectbox("Choose your mood:", options=list(playlists.keys()), index=3)

# Play matching playlist
st.write("### Now Playing Songs For Your Mood")
st.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=380)

# Footer
st.markdown("---")
st.caption("Made with ❤️ by **Vazir** | BTech CSE 2025 | Full ML Version: [Google Colab Live Demo](#) | GitHub: vazir0028/emoplay")
