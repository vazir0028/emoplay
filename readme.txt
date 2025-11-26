import importlib
import cv2
import numpy as np
import os

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

# Prefer the real `deepface` package when available. If not present we
# will fall back to the local stub (added to this repo) so the app
# remains runnable for demos. If the local stub is being used the UI
# shows a non-blocking warning suggesting installation of the real
# package for full functionality.
DeepFace = None
try:
    from deepface import DeepFace as _DeepFaceClass
    DeepFace = _DeepFaceClass
    # Detect whether the imported `deepface` module is the local stub
    # included in the project. If so, show a warning so the user can
    # replace it with the real package when they're ready.
    try:
        import deepface as _deepface_mod
        _mod_path = getattr(_deepface_mod, "__file__", "") or ""
        _local_expected = os.path.abspath(os.path.join(os.path.dirname(__file__), "deepface", "__init__.py"))
        if os.path.abspath(_mod_path) == _local_expected:
            try:
                st.warning("Using local deepface stub. Install the real `deepface` package and remove the local `deepface/` folder for full functionality.")
            except Exception:
                pass
    except Exception:
        # If we can't introspect, continue silently — we still have DeepFace
        pass
except Exception:
    DeepFace = None

st.set_page_config(page_title="EmoPlay", layout="centered")
st.set_page_config(page_title="EmoPlay", layout="centered")

# --- UI Helpers & Design -------------------------------------------------
def _css():
    return """
    <style>
    * {font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif}
    body {background:#f8f9fa; color:#2c3e50}
    .app-header{display:flex;align-items:center;gap:16px; margin-bottom:32px}
    .logo{font-size:48px}
    .app-header h1 {color:#1a73e8; margin:0; font-size:32px; font-weight:700}
    .app-header .muted {color:#666; font-size:14px; margin-top:4px}
    .card{
      background:#fff;
      padding:24px;
      border-radius:8px;
      border:1px solid #e0e0e0;
      box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }
    .emotion-bubble{
      display:inline-block;
      padding:12px 24px;
      border-radius:20px;
      font-weight:600;
      color:#fff;
      font-size:24px;
    }
    .center{display:flex;align-items:center;justify-content:center; flex-direction:column}
    .muted{color:#666; font-size:13px}
    .playlist-link {
      display:inline-block;
      padding:12px 28px;
      background:#1a73e8;
      color:#fff;
      text-decoration:none;
      border:none;
      border-radius:6px;
      font-weight:600;
      font-size:14px;
      cursor:pointer;
      transition:all 0.2s;
      margin:16px 0;
    }
    .playlist-link:hover {
      background:#1557b0;
      transform:translateY(-2px);
      box-shadow:0 4px 12px rgba(26, 115, 232, 0.3);
    }
    .history-item {color:#2c3e50; margin:8px 0; font-size:13px}
    </style>
    """


st.markdown(_css(), unsafe_allow_html=True)
st.markdown('<div class="app-header"><div class="logo">🎧</div><div><h1 style="margin:0">EmoPlay</h1><div class="muted">Music that matches your mood</div></div></div>', unsafe_allow_html=True)
st.markdown("---")
st.write("Allow camera → look at webcam → songs change with your emotion!")

playlists = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned",
    "disgust": "https://open.spotify.com/playlist/37i9dQZF1DWYNSmSSRFIWg"
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
    
    # Left column: emotion display only (no captured image)

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
    left.markdown(f"<div class=\"card center\"><div style=\"text-align:center\"><div class=\"emotion-bubble\" style=\"background:{color}\">{emoji} &nbsp; {emotion.upper()}</div><div class=\"muted\" style=\"margin-top:12px\">Detected mood</div></div></div>", unsafe_allow_html=True)

    # Confidence meter
    pct = int(emotion_confidence) if emotion_confidence else 0
    meter_html = f"""
    <div style='margin-top:16px'>
      <div style='font-size:12px;color:#666;margin-bottom:8px;font-weight:600'>Confidence: {pct}%</div>
      <div style='background:#e0e0e0;border-radius:4px;height:8px;width:100%'><div style='width:{pct}%;background:linear-gradient(90deg,#1a73e8,#ea4335);height:8px;border-radius:4px;transition:width 0.3s'></div></div>
    </div>
    """
    left.markdown(meter_html, unsafe_allow_html=True)

    # Right column: Spotify link
    right.markdown('<div class="card"><h3 style="margin:0;color:#1a73e8">▶ NOW PLAYING ◀</h3><div class="muted" style="margin-top:6px">Perfect songs for your mood</div></div>', unsafe_allow_html=True)
    
    # Open in Spotify link
    src = playlists.get(emotion, playlists["neutral"]) or playlists["neutral"]
    right.markdown(f'<a href="{src}" target="_blank" class="playlist-link">🎵 Open in Spotify</a>', unsafe_allow_html=True)

    # Mood history and simple counts
    right.markdown('<div style="margin-top:16px" class="card"><h4 style="margin:0;color:#1a73e8">📊 Recent Moods</h4></div>', unsafe_allow_html=True)
    # show recent entries
    rows = []
    for entry in hist[:6]:
        e = entry['emotion']
        c = entry.get('confidence', 0)
        emo_ico = EMOJI.get(e, ('😐', '#9AA0FF'))[0]
        rows.append(f'<div class="history-item">{emo_ico} {e.upper()} — {c}%</div>')
    right.markdown(''.join(rows), unsafe_allow_html=True)

    # counts
    counts = {}
    for entry in hist:
        counts[entry['emotion']] = counts.get(entry['emotion'], 0) + 1
    if counts:
        right.markdown('<div style="margin-top:12px" class="card"><b style="color:#1a73e8">Mood Counts</b></div>', unsafe_allow_html=True)
        right.markdown(' · '.join([f"**{k}**: {v}" for k, v in counts.items()]))

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
    left.markdown('<div class="card center"><h3 style="margin:0;color:#1a73e8">Waiting for camera</h3><div class="muted" style="margin-top:8px">Click the camera icon above to begin</div></div>', unsafe_allow_html=True)
    right.markdown('<div class="card center"><h3 style="margin:0;color:#1a73e8">No playlist yet</h3><div class="muted" style="margin-top:8px">Allow camera to see your mood-matched playlist</div></div>', unsafe_allow_html=True)
