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
    :root{--accent:#00ff41; --accent-2:#ff006e; --dark-bg:#0a0e27; --card-bg:#1a1f3a}
    * {font-family: 'Courier New', monospace}
    body {background:#0a0e27; color:#00ff41}
    .app-header{display:flex;align-items:center;gap:12px; margin-bottom:24px}
    .logo{font-size:48px; text-shadow:0 0 20px #ff006e}
    .app-header h1 {color:#00ff41; text-shadow:0 0 10px #00ff41; margin:0; letter-spacing:3px}
    .app-header .muted {color:#00a878; text-shadow:0 0 5px #00a878}
    .card{
      background:linear-gradient(135deg, #1a1f3a 0%, #16213e 100%);
      padding:20px;
      border-radius:2px;
      border:2px solid #00ff41;
      box-shadow:0 0 20px rgba(0,255,65,0.3), inset 0 0 20px rgba(255,0,110,0.1);
      position:relative;
    }
    .card::before {content:''; position:absolute; top:0; left:0; right:0; bottom:0; background:linear-gradient(90deg, transparent 0%, rgba(0,255,65,0.1) 50%, transparent 100%); pointer-events:none; border-radius:2px}
    .emotion-bubble{
      display:inline-block;
      padding:16px 24px;
      border-radius:0px;
      font-weight:900;
      color:#000;
      border:3px solid;
      box-shadow:0 0 30px currentColor;
      text-transform:uppercase;
      letter-spacing:2px;
    }
    .center{display:flex;align-items:center;justify-content:center; flex-direction:column}
    .muted{color:#00a878; text-shadow:0 0 5px #00a878}
    .playlist-link {
      display:inline-block;
      padding:14px 24px;
      background:linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
      color:#000;
      text-decoration:none;
      border:2px solid #00ff41;
      border-radius:0px;
      font-weight:900;
      text-transform:uppercase;
      letter-spacing:2px;
      box-shadow:0 0 20px #00ff41, inset 0 0 10px rgba(255,255,255,0.3);
      transition:all 0.3s;
      margin:12px 0;
    }
    .playlist-link:hover {
      box-shadow:0 0 40px #00ff41, 0 0 60px #ff006e, inset 0 0 20px rgba(255,255,255,0.5);
      transform:scale(1.05);
      background:linear-gradient(135deg, #00ff41 0%, #ff006e 100%);
    }
    .history-item {color:#00ff41; margin:6px 0; text-shadow:0 0 5px #00ff41}
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

    emoji, color = EMOJI.get(emotion.lower(), ('😐', '#00ff41'))
    left.markdown(f"<div class=\"card center\"><div style=\"text-align:center\"><div class=\"emotion-bubble\" style=\"background:{color}; border-color:{color}\">{emoji} &nbsp; {emotion.upper()}</div><div class=\"muted\" style=\"margin-top:12px\">⚡ DETECTED MOOD ⚡</div></div></div>", unsafe_allow_html=True)

    # Confidence meter
    pct = int(emotion_confidence) if emotion_confidence else 0
    meter_html = f"""
    <div style='margin-top:16px'>
      <div style='font-size:11px;color:#00a878;margin-bottom:8px;text-transform:uppercase;letter-spacing:2px;font-weight:bold'>⚙ CONFIDENCE: {pct}% ⚙</div>
      <div style='background:#0a0e27;border-radius:0px;height:8px;width:100%;border:1px solid #00ff41;box-shadow:inset 0 0 10px rgba(0,255,65,0.3)'><div style='width:{pct}%;background:linear-gradient(90deg,#00ff41,#ff006e);height:8px;border-radius:0px;box-shadow:0 0 15px #00ff41'></div></div>
    </div>
    """
    left.markdown(meter_html, unsafe_allow_html=True)

    # Right column: Spotify link
    right.markdown('<div class="card"><h3 style="margin:0;color:#00ff41;text-shadow:0 0 10px #00ff41">▶ NOW PLAYING ◀</h3><div class="muted" style="margin-top:6px">↓ Perfect songs for your mood ↓</div></div>', unsafe_allow_html=True)
    
    # Open in Spotify link (working direct link)
    src = playlists.get(emotion, playlists["neutral"]) or playlists["neutral"]
    right.markdown(f'<a href="{src}" target="_blank" class="playlist-link">🎵 Open Playlist in Spotify 🎵</a>', unsafe_allow_html=True)
    right.markdown('<div class="muted" style="margin-top:12px;font-size:12px">⚡ CLICK TO LAUNCH PLAYLIST ⚡</div>', unsafe_allow_html=True)

    # Mood history and simple counts
    right.markdown('<div style="margin-top:16px" class="card"><h4 style="margin:0;color:#ff006e;text-shadow:0 0 10px #ff006e">📊 RECENT MOODS 📊</h4></div>', unsafe_allow_html=True)
    # show recent entries
    rows = []
    for entry in hist[:6]:
        e = entry['emotion']
        c = entry.get('confidence', 0)
        emo_ico = EMOJI.get(e, ('😐', '#00ff41'))[0]
        rows.append(f'<div class="history-item">{emo_ico}  {e.upper()} — {c}%</div>')
    right.markdown(''.join(rows), unsafe_allow_html=True)

    # counts
    counts = {}
    for entry in hist:
        counts[entry['emotion']] = counts.get(entry['emotion'], 0) + 1
    if counts:
        right.markdown('<div style="margin-top:12px; padding:12px; border:1px solid #00a878; border-radius:0px; background:rgba(0,168,120,0.1)"><div style="color:#00a878;font-weight:bold;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">📈 MOOD COUNT 📈</div>' + ''.join([f'<div style="color:#00ff41;margin:4px 0"><strong>{k}</strong>: {v}x</div>' for k, v in counts.items()]) + '</div>', unsafe_allow_html=True)

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
    left.markdown('<div class="card center"><h3 style="color:#ff006e;text-shadow:0 0 15px #ff006e;text-transform:uppercase;letter-spacing:3px">🎬 AWAITING INPUT 🎬</h3><div class="muted" style="margin-top:12px">Click the camera icon to begin emotion detection</div></div>', unsafe_allow_html=True)
    right.markdown('<div class="card center"><h3 style="color:#ff006e;text-shadow:0 0 15px #ff006e;text-transform:uppercase;letter-spacing:3px">🎵 STANDBY 🎵</h3><div class="muted" style="margin-top:12px">Playlist will appear once your mood is detected</div></div>', unsafe_allow_html=True)
