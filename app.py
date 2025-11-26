import importlib
import cv2
import numpy as np

# Dynamic import so editor warnings don't block execution when packages
# aren't installed. If a module is missing we provide a minimal runtime
# fallback so the script is still runnable for checks and basic UX.
try:
    st = importlib.import_module('streamlit')
except Exception:
    # Minimal Streamlit-like stub for editor/runtime resilience.
    class _Components:
        class v1:
            @staticmethod
            def iframe(src, height=380):
                print(f"[iframe placeholder] {src} height={height}")

    class _StreamlitStub:
        def set_page_config(self, *a, **k):
            pass

        def title(self, txt=None, *a, **k):
            print(txt or "")

        def write(self, *args, **kwargs):
            print(*args)

        def camera_input(self, *a, **k):
            # No camera in stub; return None so UI shows waiting state.
            return None

        def error(self, msg):
            print("ERROR:", msg)

        def warning(self, msg):
            print("WARNING:", msg)

        def markdown(self, txt, unsafe_allow_html=False):
            print(txt)

        def image(self, src=None, caption=None, use_column_width=False):
            print(f"[image] {caption or src}")

        def info(self, txt):
            print("INFO:", txt)

        def success(self, txt):
            print("SUCCESS:", txt)

        def button(self, txt):
            print(f"[button] {txt}")
            return False

        class _Col:
            def __init__(self, parent):
                self.parent = parent

            def write(self, *a, **k):
                print(*a)

            def markdown(self, txt, unsafe_allow_html=False):
                print(txt)

            def image(self, src=None, caption=None, use_column_width=False):
                print(f"[col image] {caption or src}")

            def info(self, txt):
                print("INFO:", txt)

        def columns(self, spec):
            # Return a tuple of simple column-like objects
            count = len(spec) if isinstance(spec, (list, tuple)) else int(spec)
            return tuple(self._Col(self) for _ in range(count))

        components = _Components()

    st = _StreamlitStub()

# Provide a basic `session_state` at module level so UI features that
# use it won't fail when Streamlit isn't installed.
st.session_state = {}

try:
    deepface_mod = importlib.import_module('deepface')
    DeepFace = getattr(deepface_mod, 'DeepFace', None)
except Exception:
    DeepFace = None

st.set_page_config(page_title="EmoPlay", layout="centered")
st.set_page_config(page_title="EmoPlay", layout="centered")

# --- UI Helpers & Design -------------------------------------------------
def _css():
    return """
    <style>
    :root{--accent:#7b61ff; --accent-2:#ff758c}
    .app-header{display:flex;align-items:center;gap:12px}
    .logo{font-size:32px}
    .card{background:linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));padding:16px;border-radius:12px;border:1px solid rgba(255,255,255,0.04);box-shadow:0 6px 18px rgba(0,0,0,0.25)}
    .emotion-bubble{display:inline-block;padding:12px 18px;border-radius:999px;font-weight:700;color:#fff}
    .center{display:flex;align-items:center;justify-content:center}
    .muted{color: #a6a6a6}
    </style>
    """


st.markdown(_css(), unsafe_allow_html=True)
st.markdown('<div class="app-header"><div class="logo">🎧</div><div><h1 style="margin:0">EmoPlay</h1><div class="muted">Music that matches your mood</div></div></div>', unsafe_allow_html=True)
st.markdown("---")
st.write("Allow camera → look at webcam → songs change with your emotion!")

playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC?utm_source=generator",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1?utm_source=generator",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg?utm_source=generator",
    "neutral": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL?utm_source=generator",
    "surprise": "https://open.spotify.com/embed/playlist/37i9dQZF1DXa2PvUpywmrr?utm_source=generator",
    "fear": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4fpCWaHOned?utm_source=generator",
    "disgust": "https://open.spotify.com/embed/playlist/37i9dQZF1DWYNSmSSRFIWg?utm_source=generator"
}

img_file_buffer = st.camera_input(" ")

# Emotion display mapping
EMOJI = {
    'happy': ('😊', '#FFD166'),
    'sad': ('😢', '#5DADEC'),
    'angry': ('😠', '#FF6B6B'),
    'neutral': ('😐', '#9AA0FF'),
    'surprise': ('😮', '#FFD58A'),
    'fear': ('😨', '#A18AFF'),
    'disgust': ('🤢', '#8AE28A')
}

# Layout: left = camera + emotion, right = playlist
cols = st.columns((1, 1))
left, right = cols[0], cols[1]

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if cv2_img is None:
        left.error("Could not decode the image from the camera.")
        emotion = "neutral"
    else:
        if DeepFace is None:
            st.warning("DeepFace is not installed — falling back to neutral mood.")
            emotion = "neutral"
        else:
            try:
                result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                # DeepFace.analyze may return a dict (single face) or a list (multiple faces)
                if isinstance(result, list) and len(result) > 0:
                    emotion = result[0].get('dominant_emotion') or result[0].get('emotion', {}).get('dominant_emotion', 'neutral')
                elif isinstance(result, dict):
                    emotion = result.get('dominant_emotion') or result.get('emotion', {}).get('dominant_emotion', 'neutral')
                else:
                    emotion = 'neutral'
            except Exception as e:
                left.warning(f"Emotion detection failed: {e}")
                emotion = "neutral"
    
    # Left column: show the captured image (or placeholder) and emotion
    if img_file_buffer is not None and cv2_img is not None:
        # show image in left column
        left.image(img_file_buffer, caption="Captured image", use_column_width=True)
    else:
        left.markdown('<div class="card center">No camera input — please allow camera above</div>', unsafe_allow_html=True)

    # Compute confidence from DeepFace result if available
    emotion_confidence = 0.0
    try:
        probs = None
        if 'result' in locals() and result is not None:
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                probs = result[0].get('emotion')
            elif isinstance(result, dict):
                probs = result.get('emotion')
        if isinstance(probs, dict):
            # DeepFace sometimes returns values as percentages (0-100) or proportions (0-1)
            val = probs.get(emotion.lower()) or max(probs.values())
            if isinstance(val, (int, float)):
                if 0 < val <= 1:
                    emotion_confidence = float(val) * 100.0
                else:
                    emotion_confidence = float(val)
    except Exception:
        emotion_confidence = 0.0

    # store history in session_state
    hist = st.session_state.get('mood_history') if isinstance(getattr(st, 'session_state', None), dict) else None
    if hist is None:
        st.session_state['mood_history'] = []
        hist = st.session_state['mood_history']
    # insert latest at front
    hist.insert(0, {'emotion': emotion, 'confidence': round(emotion_confidence, 1)})
    # keep recent 10
    if len(hist) > 10:
        hist.pop()

    emoji, color = EMOJI.get(emotion.lower(), ('😐', '#9AA0FF'))
    left.markdown(f"<div class=\"card center\"><div style=\"text-align:center\"><div class=\"emotion-bubble\" style=\"background:{color}\">{emoji} &nbsp; {emotion.upper()}</div><div class=\"muted\" style=\"margin-top:8px\">Detected mood</div></div>", unsafe_allow_html=True)

    # Confidence meter
    pct = int(emotion_confidence) if emotion_confidence else 0
    meter_html = f"""
    <div style='margin-top:12px'>
      <div style='font-size:12px;color:#9aa0ff;margin-bottom:6px'>Confidence: {pct}%</div>
      <div style='background:#eee;border-radius:8px;height:12px;width:100%'><div style='width:{pct}%;background:linear-gradient(90deg,var(--accent),var(--accent-2));height:12px;border-radius:8px'></div></div>
    </div>
    """
    left.markdown(meter_html, unsafe_allow_html=True)

    # Right column: playlist embed and description
    right.markdown('<div class="card"><h3 style="margin:0">Now Playing</h3><div class="muted">Perfect songs for your mood ↓</div></div>', unsafe_allow_html=True)
    right.components.v1.iframe(playlists.get(emotion, playlists["neutral"]), height=320)

    # Open in Spotify link (non-embed)
    src = playlists.get(emotion, playlists["neutral"]) or playlists["neutral"]
    open_url = src.replace('/embed', '')
    right.markdown(f"[Open in Spotify]({open_url})")
    right.markdown('<div class="muted" style="margin-top:8px">Tip: If the playlist doesn\'t start, open it in Spotify using the link above.</div>', unsafe_allow_html=True)

    # Mood history and simple counts
    right.markdown('<div style="margin-top:12px" class="card"><h4 style="margin:0">Recent moods</h4></div>', unsafe_allow_html=True)
    # show recent entries
    rows = []
    for entry in hist[:6]:
        e = entry['emotion']
        c = entry.get('confidence', 0)
        emo_ico = EMOJI.get(e, ('😐', '#9AA0FF'))[0]
        rows.append(f"{emo_ico}  {e.upper()} — {c}%")
    right.markdown('<br>'.join(rows))

    # counts
    counts = {}
    for entry in hist:
        counts[entry['emotion']] = counts.get(entry['emotion'], 0) + 1
    if counts:
        right.markdown('<div style="margin-top:8px" class="muted">Mood counts (recent):</div>')
        right.markdown('  '.join([f"**{k}**: {v}" for k, v in counts.items()]))

    # Dependency checker (non-invasive)
    import importlib.util
    needed = ['streamlit', 'deepface', 'cv2', 'numpy']
    missing = [m for m in needed if importlib.util.find_spec(m) is None]
    if missing:
        right.markdown('<div style="margin-top:12px" class="card"><b>Missing packages</b><div class="muted">The app may have reduced functionality without these packages.</div></div>', unsafe_allow_html=True)
        right.markdown(', '.join(missing))
        right.markdown(f"To install: `pip install {' '.join(missing)}`")
else:
    left, right = cols[0], cols[1]
    left.markdown('<div class="card center">Waiting for camera… click the camera above</div>', unsafe_allow_html=True)
    right.markdown('<div class="card center"><div class="muted">No playlist yet — allow camera to begin</div></div>', unsafe_allow_html=True)
