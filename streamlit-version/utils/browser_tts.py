"""
Browser Text-to-Speech Utilities
Provides cloud-compatible audio output using browser's native TTS
"""
import streamlit.components.v1 as components


def speak_text(text: str, rate: float = 1.0, pitch: float = 1.0, volume: float = 1.0):
    """
    Speak text using browser's native Text-to-Speech API
    Works in cloud deployment without requiring server audio hardware
    
    Args:
        text: Text to speak
        rate: Speech rate (0.1 to 10, default 1.0)
        pitch: Voice pitch (0 to 2, default 1.0)
        volume: Volume (0 to 1, default 1.0)
    
    Example:
        speak_text("Hello")
        speak_text("A", rate=0.9, pitch=1.1)
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


def stop_speech():
    """Stop any ongoing speech"""
    html_code = """
    <script>
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    </script>
    """
    components.html(html_code, height=0)
