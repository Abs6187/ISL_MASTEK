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

# Try to import gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


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
        
        # Create HTML audio element with autoplay
        if autoplay:
            md = f"""
                <audio id="tts-audio" controls autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                </audio>
                <script>
                    // Ensure audio plays (some browsers block autoplay)
                    var audio = document.getElementById('tts-audio');
                    if (audio) {{
                        audio.play().catch(function(e) {{
                            console.log('Autoplay blocked, user interaction required:', e);
                        }});
                    }}
                </script>
            """
        else:
            md = f"""
                <audio id="tts-audio" controls>
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
        
        # Create HTML audio element with visible controls
        autoplay_attr = "autoplay" if autoplay else ""
        should_autoplay = "true" if autoplay else "false"
        import random
        audio_id = f"tts-audio-visible-{random.randint(1000, 9999)}"
        md = f"""
            <div style="text-align: center; margin: 10px 0;">
                <audio id="{audio_id}" controls {autoplay_attr} style="width: 100%; max-width: 400px;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            <script>
                var audio = document.getElementById('{audio_id}');
                if (audio && {should_autoplay}) {{
                    audio.play().catch(function(e) {{
                        console.log('Autoplay blocked:', e);
                    }});
                }}
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
