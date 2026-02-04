"""
Browser Text-to-Speech Utilities
Provides cloud-compatible audio output with multiple fallback options:
1. gTTS (Google Text-to-Speech) with base64 autoplay audio - works everywhere
2. Browser's native Web Speech API as backup
"""
import streamlit as st
import streamlit.components.v1 as components
import base64
import io
import time
import hashlib

# Try to import gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Supported Indian Languages for gTTS
INDIAN_LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml",
    "Marathi (मराठी)": "mr",
    "Gujarati (ગુજરાતી)": "gu",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
}

# Letter pronunciations in different Indian languages
LETTER_PRONUNCIATIONS = {
    "en": lambda letter: f"The letter {letter}",
    "hi": lambda letter: f"अक्षर {letter}",
    "bn": lambda letter: f"অক্ষর {letter}",
    "ta": lambda letter: f"எழுத்து {letter}",
    "te": lambda letter: f"అక్షరం {letter}",
    "kn": lambda letter: f"ಅಕ್ಷರ {letter}",
    "ml": lambda letter: f"അക്ഷരം {letter}",
    "mr": lambda letter: f"अक्षर {letter}",
    "gu": lambda letter: f"અક્ષર {letter}",
    "pa": lambda letter: f"ਅੱਖਰ {letter}",
}

def get_letter_pronunciation(letter: str, lang: str = "en") -> str:
    """
    Get the pronunciation text for a letter in the specified language.
    
    Args:
        letter: The letter to pronounce (A-Z)
        lang: Language code (default 'en')
    
    Returns:
        str: The pronunciation text in the specified language
    """
    if lang in LETTER_PRONUNCIATIONS:
        return LETTER_PRONUNCIATIONS[lang](letter)
    return LETTER_PRONUNCIATIONS["en"](letter)


def get_indian_languages() -> dict:
    """Return the dictionary of supported Indian languages."""
    return INDIAN_LANGUAGES.copy()


def _generate_unique_audio_id(text: str) -> str:
    """
    Generate a unique audio ID based on text content and timestamp.
    This ensures each audio element is unique and prevents caching issues.
    """
    # Use hash of text + timestamp for uniqueness
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    timestamp = int(time.time() * 1000)
    return f"tts-audio-{text_hash}-{timestamp}"


def speak_text_gtts(text: str, lang: str = 'en', slow: bool = False, autoplay: bool = True):
    """
    Speak text using Google Text-to-Speech (gTTS) with base64 audio autoplay.
    This is the most reliable method that works in all browsers and cloud deployments.
    
    Args:
        text: Text to speak
        lang: Language code (default 'en')
        slow: Whether to speak slowly (default False)
        autoplay: Whether to autoplay the audio (default True)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not text or not GTTS_AVAILABLE:
        return False
    
    try:
        # Generate audio using gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_bytes = audio_buffer.read()
        b64 = base64.b64encode(audio_bytes).decode()
        
        # Generate unique audio ID to prevent caching
        audio_id = _generate_unique_audio_id(text)
        
        # Create HTML audio element with autoplay and cache-busting
        if autoplay:
            md = f"""
                <script>
                    // Stop and remove any previous audio elements
                    document.querySelectorAll('audio[id^="tts-audio"]').forEach(function(el) {{
                        el.pause();
                        el.currentTime = 0;
                        el.remove();
                    }});
                </script>
                <audio id="{audio_id}" controls autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                </audio>
                <script>
                    // Ensure audio plays (some browsers block autoplay)
                    var audio = document.getElementById('{audio_id}');
                    if (audio) {{
                        audio.play().catch(function(e) {{
                            console.log('Autoplay blocked, user interaction required:', e);
                        }});
                    }}
                </script>
            """
        else:
            md = f"""
                <audio id="{audio_id}" controls>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                </audio>
            """
        
        st.markdown(md, unsafe_allow_html=True)
        return True
        
    except Exception as e:
        st.warning(f"gTTS error: {str(e)}")
        return False


def speak_text_gtts_visible(text: str, lang: str = 'en', slow: bool = False, autoplay: bool = True):
    """
    Same as speak_text_gtts but shows visible audio controls.
    Uses unique IDs and cache-busting to prevent stale audio playback.
    
    Args:
        text: Text to speak
        lang: Language code (default 'en')
        slow: Whether to speak slowly (default False)
        autoplay: Whether to autoplay the audio (default True)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not text or not GTTS_AVAILABLE:
        return False
    
    try:
        # Generate audio using gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_bytes = audio_buffer.read()
        b64 = base64.b64encode(audio_bytes).decode()
        
        # Generate unique audio ID based on text content and timestamp
        audio_id = _generate_unique_audio_id(text)
        autoplay_attr = "autoplay" if autoplay else ""
        should_autoplay = "true" if autoplay else "false"
        
        md = f"""
            <script>
                // Stop and remove any previous visible audio elements to prevent caching
                document.querySelectorAll('audio[id^="tts-audio"]').forEach(function(el) {{
                    el.pause();
                    el.currentTime = 0;
                }});
                document.querySelectorAll('.tts-audio-container').forEach(function(el) {{
                    el.remove();
                }});
            </script>
            <div class="tts-audio-container" style="text-align: center; margin: 10px 0;">
                <audio id="{audio_id}" controls {autoplay_attr} style="width: 100%; max-width: 400px;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            <script>
                (function() {{
                    var audio = document.getElementById('{audio_id}');
                    if (audio && {should_autoplay}) {{
                        // Small delay to ensure DOM is ready
                        setTimeout(function() {{
                            audio.play().catch(function(e) {{
                                console.log('Autoplay blocked:', e);
                            }});
                        }}, 100);
                    }}
                }})();
            </script>
        """
        
        st.markdown(md, unsafe_allow_html=True)
        return True
        
    except Exception as e:
        st.warning(f"gTTS error: {str(e)}")
        return False


def speak_text_browser(text: str, rate: float = 1.0, pitch: float = 1.0, volume: float = 1.0):
    """
    Speak text using browser's native Text-to-Speech API (Web Speech API).
    This is a fallback option that may not work in all environments.
    
    Args:
        text: Text to speak
        rate: Speech rate (0.1 to 10, default 1.0)
        pitch: Voice pitch (0 to 2, default 1.0)
        volume: Volume (0 to 1, default 1.0)
    """
    if not text:
        return
    
    # Escape special characters for JavaScript
    text = text.replace('"', '\\"').replace("'", "\\'")
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    <script>
        (function() {{
            // Check if speech synthesis is supported
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance("{text}");
                utterance.lang = 'en-US';
                utterance.rate = {rate};
                utterance.pitch = {pitch};
                utterance.volume = {volume};
                
                // Speak the text
                window.speechSynthesis.cancel(); // Cancel any ongoing speech
                window.speechSynthesis.speak(utterance);
            }} else {{
                console.warn('Speech synthesis not supported');
            }}
        }})();
    </script>
    </body>
    </html>
    """
    
    # Render with zero height (invisible)
    components.html(html_code, height=0)


def speak_text(text: str, rate: float = 1.0, pitch: float = 1.0, volume: float = 1.0):
    """
    Main function to speak text - tries gTTS first, falls back to browser TTS.
    
    Args:
        text: Text to speak
        rate: Speech rate (used for browser TTS fallback)
        pitch: Voice pitch (used for browser TTS fallback)
        volume: Volume (used for browser TTS fallback)
    """
    if not text:
        return
    
    # Try gTTS first (more reliable)
    if GTTS_AVAILABLE:
        success = speak_text_gtts(text)
        if success:
            return
    
    # Fall back to browser TTS
    speak_text_browser(text, rate, pitch, volume)


def stop_speech():
    """Stop any ongoing browser-based speech"""
    html_code = """
    <script>
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    </script>
    """
    components.html(html_code, height=0)


def is_gtts_available():
    """Check if gTTS is available"""
    return GTTS_AVAILABLE
