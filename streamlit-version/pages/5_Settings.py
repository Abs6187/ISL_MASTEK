import streamlit as st
import streamlit.components.v1 as components
import sys
import os

# Add parent directory to path for utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Initialize session state for settings
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'standard'
if 'sample_text_loaded' not in st.session_state:
    st.session_state.sample_text_loaded = None

# Set dark theme
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# Material UI Color Schema
st.markdown("""
    <style>.floating-game-link{position:fixed;bottom:24px;right:24px;width:56px;height:56px;background:linear-gradient(135deg,#6a11cb,#2575fc);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.8rem;text-decoration:none;color:white;box-shadow:0 4px 15px rgba(0,0,0,0.3);z-index:9999;transition:transform 0.3s,box-shadow 0.3s;}.floating-game-link:hover{transform:scale(1.15);box-shadow:0 6px 20px rgba(0,0,0,0.4);}</style>
    <a href="https://isl-mastek.onrender.com/" target="_blank" class="floating-game-link" title="Open Web Game">🎮</a>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0E1117 0%, #1a1d29 50%, #262730 100%);
        }
        h1 {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 50%, #00BCD4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
        }
        .stSelectbox, .stSlider {
            color: #E0E0E0;
        }
        label {
            color: #4FC3F7 !important;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Settings")

# Model Selection Section
st.markdown("## 🧠 Recognition Model Selection")
st.info("Choose between standard MLP models or advanced deep learning model")

model_options = {
    "Standard MLP (Fast)": "standard",
    "Advanced Deep Learning (H5)": "advanced"
}

selected_model_name = st.selectbox(
    "Select Recognition Model:",
    list(model_options.keys()),
    index=0 if st.session_state.selected_model == 'standard' else 1,
    key="model_selector"
)

# Update session state
st.session_state.selected_model = model_options[selected_model_name]

if st.session_state.selected_model == 'standard':
    st.success("✅ **Standard MLP Model** - Fast inference, good accuracy for basic signs")
    st.markdown("""
    - Uses pickle-based MLP models
    - Separate models for alphabets (42/84 features) and numbers
    - Optimized for speed
    """)
else:
    st.success("🚀 **Advanced H5 Model** - Deep learning with higher accuracy")
    st.markdown("""
    - Uses TensorFlow/Keras H5 model
    - Better generalization for complex gestures
    - May be slower but more accurate
    """)
    
    # Check if H5 model exists
    h5_model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'sign_language_recognition.h5')
    if os.path.exists(h5_model_path):
        st.success(f"✅ H5 model found: sign_language_recognition.h5")
        st.info("🔧 **Note:** H5 model integration with real-time WebRTC is in progress. Currently using MLP for live recognition.")
    else:
        st.warning("⚠️ H5 model not found. Please add sign_language_recognition.h5 to assets/models/")

st.markdown("---")

# gTTS Section - More reliable
st.markdown("## 🔊 Google Text-to-Speech (gTTS)")
st.info("✅ **Recommended** - Works reliably in all browsers and cloud deployments")

# Sample texts for different languages
sample_texts = {
    "en": "Hello! This is a test of Google Text-to-Speech.",
    "hi": "नमस्ते! यह गूगल टेक्स्ट-टू-स्पीच का परीक्षण है।",
    "bn": "হ্যালো! এটি গুগল টেক্সট-টু-স্পিচের একটি পরীক্ষা।",
    "ta": "வணக்கம்! இது கூகுள் உரை-இருந்து-பேச்சு சோதனை.",
    "te": "హలో! ఇది గూగుల్ టెక్స్ట్-టు-స్పీచ్ పరీక్ష.",
    "kn": "ಹಲೋ! ಇದು ಗೂಗಲ್ ಟೆಕ್ಸ್ಟ್-ಟು-ಸ್ಪೀಚ್ ಪರೀಕ್ಷೆ.",
    "ml": "ഹലോ! ഇത് ഗൂഗിൾ ടെക്സ്റ്റ്-ടു-സ്പീച്ച് പരീക്ഷണമാണ്.",
    "mr": "नमस्कार! हे गूगल टेक्स्ट-टू-स्पीच चाचणी आहे.",
    "gu": "હેલો! આ ગૂગલ ટેક્સ્ટ-ટુ-સ્પીચ ટેસ્ટ છે.",
    "pa": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਇਹ ਗੂਗਲ ਟੈਕਸਟ-ਟੂ-ਸਪੀਚ ਦੀ ਜਾਂਚ ਹੈ।",
}

try:
    from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_indian_languages
    
    if is_gtts_available():
        # Get Indian languages
        indian_langs = get_indian_languages()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_lang_name = st.selectbox(
                "Language", 
                list(indian_langs.keys()),
                index=0,
                key="gtts_lang_selector"
            )
            gtts_lang = indian_langs[selected_lang_name]
        with col2:
            gtts_slow = st.checkbox("Slow mode", value=False, key="gtts_slow")
        with col3:
            gtts_autoplay = st.checkbox("Autoplay", value=True, key="gtts_autoplay")
        
        # Determine default text - use sample if just loaded, otherwise default
        if st.session_state.sample_text_loaded:
            default_text = sample_texts.get(st.session_state.sample_text_loaded, "Hello! This is a test of Google Text-to-Speech.")
        else:
            default_text = "Hello! This is a test of Google Text-to-Speech."
        
        gtts_text = st.text_area("Text to speak with gTTS:", value=default_text, height=100, key="gtts_text_area")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(f"📝 Load {selected_lang_name} Sample", key="load_sample"):
                st.session_state.sample_text_loaded = gtts_lang
                st.rerun()
        
        with col_btn2:
            if st.button("🔊 Speak with gTTS", key="speak_gtts"):
                if gtts_text:
                    # Clear the loaded sample flag
                    st.session_state.sample_text_loaded = None
                    speak_text_gtts_visible(gtts_text, lang=gtts_lang, slow=gtts_slow, autoplay=gtts_autoplay)
                else:
                    st.warning("Please enter some text to speak")
        
        # Show supported languages info
        with st.expander("ℹ️ Supported Indian Languages"):
            st.markdown("""
            | Language | Code | Script |
            |----------|------|--------|
            | English | en | Latin |
            | Hindi | hi | देवनागरी |
            | Bengali | bn | বাংলা |
            | Tamil | ta | தமிழ் |
            | Telugu | te | తెలుగు |
            | Kannada | kn | ಕನ್ನಡ |
            | Malayalam | ml | മലയാളം |
            | Marathi | mr | मराठी |
            | Gujarati | gu | ગુજરાતી |
            | Punjabi | pa | ਪੰਜਾਬੀ |
            """)
    else:
        st.warning("gTTS is not installed. Install with: pip install gTTS")
        
except ImportError as e:
    st.warning(f"Could not load gTTS module: {e}")

st.markdown("---")

# Browser TTS Section - Fallback
st.markdown("## 🌐 Browser Text-to-Speech (Fallback)")
st.info("⚠️ **Fallback option** - Uses browser's built-in TTS, may not work in all environments")

# Use components.html() for complex HTML with JavaScript (renders in iframe)
browser_tts_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #0E1117;
            margin: 0;
            padding: 10px;
        }
        .tts-container {
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
        }
        .control-group {
            margin: 15px 0;
            padding: 12px;
            background: #1E1E1E;
            border-radius: 8px;
            border: 1px solid #00BCD4;
        }
        .control-label {
            color: #4FC3F7;
            font-weight: 500;
            margin-bottom: 8px;
            display: block;
            font-size: 14px;
        }
        #text-input {
            width: 100%;
            min-height: 80px;
            padding: 12px;
            font-size: 14px;
            background: #2A2A2A;
            color: #E0E0E0;
            border: 2px solid #00BCD4;
            border-radius: 8px;
            margin: 8px 0;
            box-sizing: border-box;
            resize: vertical;
        }
        select, input[type="range"] {
            width: 100%;
            padding: 8px;
            background: #2A2A2A;
            color: #E0E0E0;
            border: 1px solid #00BCD4;
            border-radius: 5px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        .btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }
        .tts-btn {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
            color: #FAFAFA;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            min-width: 100px;
        }
        .tts-btn:hover {
            background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
            transform: translateY(-1px);
        }
        .tts-btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        .preset-btn {
            background: linear-gradient(135deg, #00BCD4 0%, #0097A7 100%);
            padding: 6px 12px;
            font-size: 12px;
        }
        .preset-btn:hover {
            background: linear-gradient(135deg, #00ACC1 0%, #00838F 100%);
        }
        .status-msg {
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            text-align: center;
            font-weight: 500;
            font-size: 13px;
        }
        .status-success { background: #4CAF50; color: white; }
        .status-error { background: #f44336; color: white; }
        .status-info { background: #2196F3; color: white; }
        .value-display {
            display: inline-block;
            min-width: 40px;
            text-align: right;
            color: #00BCD4;
            font-weight: bold;
        }
        .slider-labels {
            display: flex;
            justify-content: space-between;
            color: #888;
            font-size: 11px;
            margin-top: 4px;
        }
        h3 {
            color: #00BCD4;
            text-align: center;
            margin: 0 0 10px 0;
            font-size: 16px;
        }
        p.subtitle {
            text-align: center;
            color: #E0E0E0;
            margin: 0 0 15px 0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="tts-container">
        <h3>🔊 Browser Text-to-Speech Settings</h3>
        <p class="subtitle">Configure voice, speed, pitch, and volume</p>
        
        <div id="status-msg" class="status-msg status-info">Enter text and press Speak to test</div>
        
        <div class="control-group">
            <label class="control-label">📝 Text to Speak:</label>
            <textarea id="text-input" placeholder="Enter text here...">Hello! This is a test of the browser text-to-speech system.</textarea>
        </div>
        
        <div class="control-group">
            <label class="control-label">🎤 Select Voice:</label>
            <select id="voice-select"></select>
        </div>
        
        <div class="control-group">
            <label class="control-label">⚡ Speech Rate: <span class="value-display" id="rate-value">1.0</span></label>
            <input type="range" id="rate-slider" min="0.5" max="2.0" step="0.1" value="1.0">
            <div class="slider-labels"><span>Slow</span><span>Normal</span><span>Fast</span></div>
        </div>
        
        <div class="control-group">
            <label class="control-label">🎵 Pitch: <span class="value-display" id="pitch-value">1.0</span></label>
            <input type="range" id="pitch-slider" min="0.5" max="2.0" step="0.1" value="1.0">
            <div class="slider-labels"><span>Deep</span><span>Normal</span><span>High</span></div>
        </div>
        
        <div class="control-group">
            <label class="control-label">🔊 Volume: <span class="value-display" id="volume-value">1.0</span></label>
            <input type="range" id="volume-slider" min="0.0" max="1.0" step="0.1" value="1.0">
            <div class="slider-labels"><span>Quiet</span><span>Medium</span><span>Loud</span></div>
        </div>
        
        <div class="btn-group">
            <button class="tts-btn" id="speak-btn" onclick="speakText()">🔊 Speak</button>
            <button class="tts-btn" id="stop-btn" onclick="stopSpeaking()">⏹️ Stop</button>
        </div>
        
        <div class="control-group">
            <label class="control-label">🎯 Quick Presets:</label>
            <div class="btn-group">
                <button class="tts-btn preset-btn" onclick="applyPreset('normal')">Normal</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('slow')">Slow</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('fast')">Fast</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('deep')">Deep</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('high')">High</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('whisper')">Whisper</button>
            </div>
        </div>
    </div>
    
    <script>
        let synth = window.speechSynthesis;
        let voices = [];
        
        function loadVoices() {
            voices = synth.getVoices();
            const voiceSelect = document.getElementById('voice-select');
            voiceSelect.innerHTML = '';
            
            voices.forEach((voice, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = voice.name + ' (' + voice.lang + ')';
                if (voice.default) option.textContent += ' - DEFAULT';
                voiceSelect.appendChild(option);
            });
        }
        
        loadVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = loadVoices;
        }
        
        document.getElementById('rate-slider').oninput = function() {
            document.getElementById('rate-value').textContent = this.value;
        };
        document.getElementById('pitch-slider').oninput = function() {
            document.getElementById('pitch-value').textContent = this.value;
        };
        document.getElementById('volume-slider').oninput = function() {
            document.getElementById('volume-value').textContent = this.value;
        };
        
        function speakText() {
            const text = document.getElementById('text-input').value.trim();
            if (!text) {
                showStatus('Please enter some text to speak', 'error');
                return;
            }
            
            synth.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            
            const selectedVoice = document.getElementById('voice-select').value;
            if (voices[selectedVoice]) utterance.voice = voices[selectedVoice];
            
            utterance.rate = parseFloat(document.getElementById('rate-slider').value);
            utterance.pitch = parseFloat(document.getElementById('pitch-slider').value);
            utterance.volume = parseFloat(document.getElementById('volume-slider').value);
            
            utterance.onstart = function() {
                showStatus('🔊 Speaking...', 'info');
                document.getElementById('speak-btn').disabled = true;
                document.getElementById('stop-btn').disabled = false;
            };
            utterance.onend = function() {
                showStatus('✅ Finished speaking', 'success');
                document.getElementById('speak-btn').disabled = false;
                document.getElementById('stop-btn').disabled = true;
            };
            utterance.onerror = function(event) {
                showStatus('❌ Error: ' + event.error, 'error');
                document.getElementById('speak-btn').disabled = false;
                document.getElementById('stop-btn').disabled = true;
            };
            
            synth.speak(utterance);
        }
        
        function stopSpeaking() {
            synth.cancel();
            showStatus('⏹️ Stopped', 'info');
            document.getElementById('speak-btn').disabled = false;
            document.getElementById('stop-btn').disabled = true;
        }
        
        function showStatus(message, type) {
            const statusMsg = document.getElementById('status-msg');
            statusMsg.textContent = message;
            statusMsg.className = 'status-msg status-' + type;
        }
        
        function applyPreset(preset) {
            const rateSlider = document.getElementById('rate-slider');
            const pitchSlider = document.getElementById('pitch-slider');
            const volumeSlider = document.getElementById('volume-slider');
            
            const presets = {
                'normal': [1.0, 1.0, 1.0],
                'slow': [0.7, 1.0, 1.0],
                'fast': [1.5, 1.0, 1.0],
                'deep': [0.9, 0.5, 1.0],
                'high': [1.1, 2.0, 1.0],
                'whisper': [0.8, 0.8, 0.3]
            };
            
            if (presets[preset]) {
                rateSlider.value = presets[preset][0];
                pitchSlider.value = presets[preset][1];
                volumeSlider.value = presets[preset][2];
                
                rateSlider.dispatchEvent(new Event('input'));
                pitchSlider.dispatchEvent(new Event('input'));
                volumeSlider.dispatchEvent(new Event('input'));
                
                showStatus('✅ Applied ' + preset + ' preset', 'success');
            }
        }
        
        if (!('speechSynthesis' in window)) {
            showStatus('❌ Text-to-speech not supported in this browser', 'error');
            document.getElementById('speak-btn').disabled = true;
        }
    </script>
</body>
</html>
"""

# Render the HTML in an iframe using components.html()
components.html(browser_tts_html, height=750, scrolling=True)

st.markdown("---")

# Feedback Popup Section
st.markdown("## 💬 Feedback & Support")

# Create a popup-style expander
with st.expander("📝 Send Feedback (Click to Open)", expanded=False):
    st.markdown("""
    <style>
        .feedback-container {
            background: linear-gradient(135deg, #1E1E1E 0%, #2A2A3A 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #00BCD4;
        }
    </style>
    """, unsafe_allow_html=True)
    
    feedback_type = st.selectbox(
        "Feedback Type:",
        ["Bug Report", "Feature Request", "General Feedback", "Question"],
        key="feedback_type"
    )
    
    feedback_text = st.text_area(
        "Your Feedback:",
        placeholder="Describe your feedback here...",
        height=150,
        key="feedback_text"
    )
    
    feedback_email = st.text_input(
        "Your Email (optional):",
        placeholder="your@email.com",
        key="feedback_email"
    )
    
    if st.button("📤 Submit Feedback", key="submit_feedback"):
        if feedback_text:
            st.success("✅ Thank you for your feedback! We appreciate your input.")
            st.balloons()
            # In a real app, you would send this to a backend/email service
        else:
            st.warning("Please enter some feedback before submitting.")

# Info about port 5000 API (if applicable)
with st.expander("🔌 API Server Info", expanded=False):
    st.markdown("""
    ### Backend API Server
    
    If you're running the web game version, a Flask API server runs on **port 5000**.
    
    **Endpoints:**
    - `POST /predict` - Sign language recognition
    - `GET /health` - Health check
    
    **Example:**
    ```bash
    curl -X POST http://localhost:5000/predict \
        -H "Content-Type: application/json" \
        -d '{"landmarks": [...]}'
    ```
    
    *Note: The Streamlit Cloud version uses browser-based processing and doesn't require the API server.*
    """)
