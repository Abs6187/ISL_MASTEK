import streamlit as st
import sys
import os

# Add parent directory to path for utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set dark theme
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")

# Material UI Color Schema
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

# gTTS Section - More reliable
st.markdown("## 🔊 Google Text-to-Speech (gTTS)")
st.info("✅ **Recommended** - Works reliably in all browsers and cloud deployments")

try:
    from utils.browser_tts import speak_text_gtts_visible, is_gtts_available
    
    if is_gtts_available():
        gtts_text = st.text_input("Text to speak with gTTS:", value="Hello! This is a test of Google Text-to-Speech.", key="gtts_text")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            gtts_lang = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "it", "pt", "ja", "ko", "zh-CN"], key="gtts_lang")
        with col2:
            gtts_slow = st.checkbox("Slow mode", value=False, key="gtts_slow")
        with col3:
            gtts_autoplay = st.checkbox("Autoplay", value=True, key="gtts_autoplay")
        
        if st.button("🔊 Speak with gTTS", key="speak_gtts"):
            if gtts_text:
                speak_text_gtts_visible(gtts_text, lang=gtts_lang, slow=gtts_slow, autoplay=gtts_autoplay)
            else:
                st.warning("Please enter some text to speak")
    else:
        st.warning("gTTS is not installed. Install with: pip install gTTS")
        
except ImportError as e:
    st.warning(f"Could not load gTTS module: {e}")

st.markdown("---")

# Browser TTS Section - Fallback
st.markdown("## 🌐 Browser Text-to-Speech (Fallback)")
st.info("⚠️ **Fallback option** - Uses browser's built-in TTS, may not work in all environments")
st.markdown("""
    <style>
        .tts-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        .control-group {
            margin: 20px 0;
            padding: 15px;
            background: #1E1E1E;
            border-radius: 8px;
            border: 1px solid #00BCD4;
        }
        .control-label {
            color: #4FC3F7;
            font-weight: 500;
            margin-bottom: 10px;
            display: block;
        }
        #text-input {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            font-size: 16px;
            background: #2A2A2A;
            color: #E0E0E0;
            border: 2px solid #00BCD4;
            border-radius: 8px;
            margin: 10px 0;
        }
        select, input[type="range"] {
            width: 100%;
            padding: 10px;
            background: #2A2A2A;
            color: #E0E0E0;
            border: 1px solid #00BCD4;
            border-radius: 5px;
            margin: 10px 0;
        }
        .btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        .tts-btn {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
            color: #FAFAFA;
            border: none;
            border-radius: 8px;
            padding: 12px 25px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            min-width: 120px;
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
            padding: 8px 15px;
            font-size: 14px;
        }
        .preset-btn:hover {
            background: linear-gradient(135deg, #00ACC1 0%, #00838F 100%);
        }
        .status-msg {
            padding: 12px;
            margin: 10px 0;
            border-radius: 5px;
            text-align: center;
            font-weight: 500;
        }
        .status-success {
            background: #4CAF50;
            color: white;
        }
        .status-error {
            background: #f44336;
            color: white;
        }
        .status-info {
            background: #2196F3;
            color: white;
        }
        .value-display {
            display: inline-block;
            min-width: 50px;
            text-align: right;
            color: #00BCD4;
            font-weight: bold;
        }
    </style>
    
    <div class="tts-container">
        <h2 style="color: #00BCD4; text-align: center;">🔊 Browser Text-to-Speech Settings</h2>
        <p style="text-align: center; color: #E0E0E0;">Configure voice, speed, pitch, and volume using your browser's built-in TTS</p>
        
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
            <div style="display: flex; justify-content: space-between; color: #888; font-size: 12px;">
                <span>Slow (0.5)</span>
                <span>Normal (1.0)</span>
                <span>Fast (2.0)</span>
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label">🎵 Pitch: <span class="value-display" id="pitch-value">1.0</span></label>
            <input type="range" id="pitch-slider" min="0.5" max="2.0" step="0.1" value="1.0">
            <div style="display: flex; justify-content: space-between; color: #888; font-size: 12px;">
                <span>Deep (0.5)</span>
                <span>Normal (1.0)</span>
                <span>High (2.0)</span>
            </div>
        </div>
        
        <div class="control-group">
            <label class="control-label">🔊 Volume: <span class="value-display" id="volume-value">1.0</span></label>
            <input type="range" id="volume-slider" min="0.0" max="1.0" step="0.1" value="1.0">
            <div style="display: flex; justify-content: space-between; color: #888; font-size: 12px;">
                <span>Quiet (0.0)</span>
                <span>Medium (0.5)</span>
                <span>Loud (1.0)</span>
            </div>
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
                <button class="tts-btn preset-btn" onclick="applyPreset('deep')">Deep Voice</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('high')">High Voice</button>
                <button class="tts-btn preset-btn" onclick="applyPreset('whisper')">Whisper</button>
            </div>
        </div>
    </div>
    
    <script>
        let synth = window.speechSynthesis;
        let voices = [];
        
        // Load voices
        function loadVoices() {
            voices = synth.getVoices();
            const voiceSelect = document.getElementById('voice-select');
            voiceSelect.innerHTML = '';
            
            voices.forEach((voice, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = voice.name + ' (' + voice.lang + ')';
                if (voice.default) {
                    option.textContent += ' - DEFAULT';
                }
                voiceSelect.appendChild(option);
            });
        }
        
        // Load voices on page load and when they change
        loadVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = loadVoices;
        }
        
        // Update slider value displays
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
            
            // Cancel any ongoing speech
            synth.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Get selected voice
            const selectedVoice = document.getElementById('voice-select').value;
            if (voices[selectedVoice]) {
                utterance.voice = voices[selectedVoice];
            }
            
            // Set parameters
            utterance.rate = parseFloat(document.getElementById('rate-slider').value);
            utterance.pitch = parseFloat(document.getElementById('pitch-slider').value);
            utterance.volume = parseFloat(document.getElementById('volume-slider').value);
            
            // Event handlers
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
            
            // Speak
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
            
            switch(preset) {
                case 'normal':
                    rateSlider.value = 1.0;
                    pitchSlider.value = 1.0;
                    volumeSlider.value = 1.0;
                    break;
                case 'slow':
                    rateSlider.value = 0.7;
                    pitchSlider.value = 1.0;
                    volumeSlider.value = 1.0;
                    break;
                case 'fast':
                    rateSlider.value = 1.5;
                    pitchSlider.value = 1.0;
                    volumeSlider.value = 1.0;
                    break;
                case 'deep':
                    rateSlider.value = 0.9;
                    pitchSlider.value = 0.5;
                    volumeSlider.value = 1.0;
                    break;
                case 'high':
                    rateSlider.value = 1.1;
                    pitchSlider.value = 2.0;
                    volumeSlider.value = 1.0;
                    break;
                case 'whisper':
                    rateSlider.value = 0.8;
                    pitchSlider.value = 0.8;
                    volumeSlider.value = 0.3;
                    break;
            }
            
            // Trigger input events to update displays
            rateSlider.dispatchEvent(new Event('input'));
            pitchSlider.dispatchEvent(new Event('input'));
            volumeSlider.dispatchEvent(new Event('input'));
            
            showStatus('✅ Applied ' + preset + ' preset', 'success');
        }
        
        // Check browser support
        if (!('speechSynthesis' in window)) {
            showStatus('❌ Text-to-speech not supported in this browser', 'error');
            document.getElementById('speak-btn').disabled = true;
        }
    </script>
""", unsafe_allow_html=True)
