# app.py - EmoPlay: Emotion-Based Music Player
# Author: Vazir | B.Tech CSE 2025

import streamlit as st
import random
import io
from PIL import Image, ImageDraw # Used for simulating drawing on an image

# --- CONFIGURATION ---
st.set_page_config(
    page_title="EmoPlay - Music for Your Mood (Bollywood Edition)",
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

# Bollywood Playlist Mapping (Simulated/Placeholder Links)
BOLLYWOOD_PLAYLISTS = {
    "happy":    "http://googleusercontent.com/spotify.com/bollywood_happy",    # Example: Balam Pichkari, Badtameez Dil
    "sad":      "http://googleusercontent.com/spotify.com/bollywood_sad",      # Example: Channa Mereya, Tujhe Bhula Diya
    "angry":    "http://googleusercontent.com/spotify.com/bollywood_angry",    # Example: Aarambh Hai Prachand, Sadda Haq
    "neutral":  "http://googleusercontent.com/spotify.com/bollywood_chill",    # Example: Khwabon Ke Parindey, Dil Chahta Hai
    "surprise": "http://googleusercontent.com/spotify.com/bollywood_energetic",# Example: Gallan Goodiyaan, Kar Gayi Chull
    "fear":     "http://googleusercontent.com/spotify.com/bollywood_dark",     # Example: Gali Gali, Raat Ka Nasha
    "disgust":  "http://googleusercontent.com/spotify.com/bollywood_heavy"     # Example: Emotional/Heavy songs like angry/sad
}

# --- SIMULATED COMPUTER VISION ANALYSIS ---
def analyze_image_for_cv_features(image_file):
    """Simulate emotion detection and confidence."""
    mask_present = random.random() < 0.2
    mood = random.choice(list(INT_PLAYLISTS.keys())) # Use INT_PLAYLISTS keys for mood simulation
    confidence = round(random.uniform(0.60, 0.99), 2)
    return mood, confidence, mask_present

# **NEW FEATURE: SIMULATED FACE DETECTION AND DRAWING**
def draw_face_circle_on_image(image_bytes):
    """
    SIMULATION FUNCTION: In a real application, this would use OpenCV or similar
    to detect a face and draw a circle around it.
    Here, we'll draw a circle in a generic position to simulate detection.
    """
    if image_bytes is None:
        return None

    # Open the image using PIL (Pillow)
    image = Image.open(image_bytes)
    draw = ImageDraw.Draw(image)

    # Simulate a face detection bounding box (x1, y1, x2, y2)
    # These coordinates are arbitrary for simulation.
    # In a real app, these would come from your face detection model.
    img_width, img_height = image.size
    
    # Let's try to center the simulated face a bit
    face_size_factor = 0.4 # Face takes up about 40% of the image width
    face_width = int(img_width * face_size_factor)
    face_height = int(img_height * face_size_factor)

    # Center the face roughly in the middle
    x_center = img_width // 2
    y_center = img_height // 2
    
    x1 = x_center - face_width // 2
    y1 = y_center - face_height // 2
    x2 = x_center + face_width // 2
    y2 = y_center + face_height // 2

    # Draw a green circle (or ellipse)
    # Using ellipse to draw a circle for simplicity with bounding box
    draw.ellipse([(x1, y1), (x2, y2)], outline="green", width=5)

    # Save the modified image to a bytes buffer to display in Streamlit
    buf = io.BytesIO()
    image.save(buf, format="PNG") # Use PNG to support transparency if needed
    buf.seek(0)
    return buf
# --- END SIMULATION ---

# --- APP LAYOUT ---

st.title("EmoPlay 🎶")
st.markdown("### Let your face choose the music")

genre_choice = st.radio(
    "Choose Your Vibe:",
    options=["International Hits", "Bollywood"],
    horizontal=True,
    index=1
)
CURRENT_PLAYLISTS = BOLLYWOOD_PLAYLISTS if genre_choice == "Bollywood" else INT_PLAYLISTS

st.write("Take a selfie or select your current mood — matching playlist starts instantly.")

# Camera input
img_file_buffer = st.camera_input("📸 Take a selfie for automatic mood detection")
mood = None # Initialize mood variable

if img_file_buffer:
    # **NEW FEATURE INTEGRATION: Draw circle on the captured image**
    processed_image_buffer = draw_face_circle_on_image(img_file_buffer)
    st.image(processed_image_buffer, use_column_width=True)
    
    # Run the simulated analysis
    detected_mood, confidence, mask_present = analyze_image_for_cv_features(img_file_buffer)

    if mask_present:
        st.warning(
            "⚠️ **Mask Detected!** Emotion detection may be unreliable. "
            "Please remove your mask for accurate analysis or select your mood manually."
        )
        mood = st.selectbox("How are you feeling right now?", options=list(CURRENT_PLAYLISTS.keys()), index=3)
        st.info("Using manually selected mood.")

    else:
        mood = detected_mood
        st.success(f"✅ Detected mood: **{mood.upper()}**")
        
        st.metric(label="Detection Confidence", value=f"{int(confidence*100)}%")
        st.progress(confidence, text="Confidence Level")

else:
    st.info("Or select your mood manually below")
    mood = st.selectbox("How are you feeling right now?", options=list(CURRENT_PLAYLISTS.keys()), index=3)

# Display and play the matching playlist
if mood:
    st.markdown("---")
    st.markdown(f"### Now Playing: **{mood.upper()} {genre_choice} Playlist** ▶️")
    st.components.v1.iframe(CURRENT_PLAYLISTS[mood], height=380)

# Footer
st.markdown("---")
st.caption("Built by **Vazir** • B.Tech CSE 2025 | Full ML + Live Webcam version available on Google Colab")
