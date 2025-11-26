!pip install deepface
!pip install spotipy

import cv2
import numpy as np
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import display, Javascript, Image
from google.colab.output import eval_js
from base64 import b64decode
import io
from PIL import Image as PILImage

# ---------------------------------------------------------
# 1. SETUP SPOTIFY
# ---------------------------------------------------------
# Replace these with your actual keys from Spotify Developer Dashboard
print("--- Spotify Setup ---")
CLIENT_ID = input("Enter your Spotify Client ID: ")
CLIENT_SECRET = input("Enter your Spotify Client Secret: ")

try:
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("✅ Spotify Connected Successfully!\n")
except Exception as e:
    print(f"❌ Spotify Connection Failed: {e}")

# ---------------------------------------------------------
# 2. DEFINE WEBCAM HELPER (JavaScript for Colab)
# ---------------------------------------------------------
def take_photo(filename='photo.jpg', quality=0.8):
  """
  Accesses the local webcam via JavaScript, captures an image,
  and saves it to the Colab filesystem.
  """
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture Emotion';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])

  # Save binary data to file
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

# ---------------------------------------------------------
# 3. MAIN APPLICATION LOOP
# ---------------------------------------------------------
def recommend_music_based_on_emotion():
    print("📸 Please click 'Capture Emotion' below...")

    try:
        # 1. Capture Image
        filename = take_photo()
        print("✅ Image captured!")

        # 2. Analyze Emotion
        print("🔍 Analyzing face...")
        obj = DeepFace.analyze(img_path = filename, actions = ['emotion'], enforce_detection=False)

        # DeepFace returns a list of dictionaries
        dominant_emotion = obj[0]['dominant_emotion']
        print(f"\n🧠 Detected Emotion: {dominant_emotion.upper()}")

        # 3. Search Spotify
        # We map emotions to search queries
        search_query = f"{dominant_emotion} hits"

        if dominant_emotion == "sad":
            search_query = "uplifting pop" # Maybe cheer them up?
        elif dominant_emotion == "angry":
            search_query = "calm relaxing"
        elif dominant_emotion == "neutral":
            search_query = "lofi study"

        print(f"🎵 Searching Spotify for: '{search_query}'...")

        results = sp.search(q=search_query, type='playlist', limit=3)

        # 4. Display Results
        print("\n🎧 Recommended Playlists:")
        playlists = results['playlists']['items']

        if not playlists:
            print("No playlists found.")
        else:
            for idx, playlist in enumerate(playlists):
                print(f"{idx+1}. {playlist['name']} - {playlist['external_urls']['spotify']}")

        # Display the captured image
        display(PILImage.open(filename))

    except Exception as e:
        print(f"❌ Error: {e}")

# Run the app
recommend_music_based_on_emotion()
