
import streamlit as st
from deepface import DeepFace
import os

# Hide warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

st.set_page_config(page_title="EmoPlay", page_icon="musical_note", layout="centered")

st.title("EmoPlay")
st.markdown("### Let your face choose the music")

# Spotify Playlists
PLAYLISTS = {
    "happy":    "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad":      "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry":    "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral":  "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear":     "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust":  "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg"
}

img_file = st.camera_input("Take a selfie (clear face, no mask/glasses for best result)")

if img_file:
    st.image(img_file, use_column_width=True)

    with st.spinner("Detecting your mood..."):
        try:
            # DeepFace directly accepts bytes → NO cv2 needed!
            result = DeepFace.analyze(
                img_path=img_file.getvalue(),   # ← Yeh line magic hai
                actions=['emotion'],
                enforce_detection=False,
                detector_backend="opencv",
                silent=True
            )[0]

            mood = result["dominant_emotion"].lower()
            emotions = result["emotion"]

            st.success(f"Detected Mood: **{mood.upper()}**")

            # Show percentages
            st.subheader("Emotion Breakdown")
            for emo, perc in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                st.write(f"**{emo.capitalize()}**: {perc:.1f}%")
                st.progress(perc / 100)

            # Smart warning for mask/glasses/low confidence
            if max(emotions.values()) < 55 or emotions["neutral"] > 40:
                st.warning("Low confidence → Remove mask, glasses, or try better lighting")

        except:
            st.error("No face detected. Try a clearer selfie!")
            mood = "neutral"
else:
    st.info("Or select manually")
    mood = st.selectbox("How are you feeling?", PLAYLISTS.keys(), index=3)

# Play music
st.markdown("### Now Playing")
st.components.v1.iframe(PLAYLISTS[mood], height=380)

# Footer
st.markdown("---")
st.caption("Made with love by Vazir • B.Tech CSE 2025 | Real AI Emotion Detection")
