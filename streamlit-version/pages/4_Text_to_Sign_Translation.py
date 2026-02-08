import streamlit as st
import os
import sys

# Add parent directory to path for utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

st.set_page_config(page_title="Text to Sign Language", page_icon="📝", layout="wide")

# Initialize session state for audio tracking and language
if 'tts_current_letter' not in st.session_state:
    st.session_state.tts_current_letter = None
if 'tts_audio_key' not in st.session_state:
    st.session_state.tts_audio_key = 0
if 'tts_language' not in st.session_state:
    st.session_state.tts_language = "en"
if 'show_sign_result' not in st.session_state:
    st.session_state.show_sign_result = False
if 'current_sign_letter' not in st.session_state:
    st.session_state.current_sign_letter = None

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
        h1, h2, h6 {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 50%, #00BCD4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        }
        p, li {
            color: #E0E0E0;
            line-height: 1.7;
        }
        .stButton > button {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
            color: #FAFAFA;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
            transform: translateY(-1px);
        }
    </style>
    <h1 style="text-align: center;">Text to Sign Language Conversion (Single Alphabet/Digit)</h1>
    <h6 style="text-align: center;">
        This feature converts a single alphabet or digit entered by the user into its corresponding Indian Sign Language (ISL) gesture representation.
    </h6>
    """, unsafe_allow_html=True)

# Language selection for audio pronunciation
st.markdown("### 🌐 Language Settings")
try:
    from utils.browser_tts import get_indian_languages, is_gtts_available
    if is_gtts_available():
        languages = get_indian_languages()
        selected_lang_name = st.selectbox(
            "Select language for audio pronunciation:",
            list(languages.keys()),
            index=0,
            key="lang_selector"
        )
        st.session_state.tts_language = languages[selected_lang_name]
    else:
        st.info("gTTS not available - audio will use English")
except ImportError:
    st.info("Language module not available")

st.markdown("---")

text = st.text_input('Enter text here:', '')
text = text.lower()

def load_image(file_name):
    """
    Load image file with case-insensitive matching.
    Handles mixed case file extensions (.jpg, .JPG, .Jpg, etc.)
    """
    folder_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
    
    # Get the base name without extension
    base_name = file_name.rsplit('.', 1)[0] if '.' in file_name else file_name
    
    # Try to find the file with case-insensitive matching
    if os.path.exists(folder_path):
        for actual_file in os.listdir(folder_path):
            actual_base = actual_file.rsplit('.', 1)[0] if '.' in actual_file else actual_file
            actual_ext = actual_file.rsplit('.', 1)[1].lower() if '.' in actual_file else ''
            
            # Match base name (case-insensitive) and check for image extensions
            if actual_base.lower() == base_name.lower() and actual_ext in ['jpg', 'jpeg', 'png', 'gif']:
                return os.path.join(folder_path, actual_file)
    
    return None 

# Create placeholders for results
audio_placeholder = st.empty()
image_placeholder = st.empty()

# Button row
col1, col2 = st.columns([1, 1])
with col1:
    generate_btn = st.button('🎯 Generate Sign', use_container_width=True)
with col2:
    clear_btn = st.button('🗑️ Clear All', use_container_width=True)

# Handle clear button
if clear_btn:
    st.session_state.tts_current_letter = None
    st.session_state.tts_audio_key += 1
    st.session_state.show_sign_result = False
    st.session_state.current_sign_letter = None
    audio_placeholder.empty()
    image_placeholder.empty()
    st.rerun()

if generate_btn:
    if text == '':
        st.write('Please enter some text.')
    elif len(text.split()) > 1:
        st.write('Please enter only one letter.')

    elif text.isalpha() == False and text.isdigit() == False:
        st.write('Please enter only alphabets.')

    else:
        st.write('Generating image...')

        # Load the image
        image = load_image(text + '.jpg')
        if image is None:
            st.write('Image not found. Please try again.')
        else:
            # Store state
            st.session_state.show_sign_result = True
            st.session_state.current_sign_letter = text.upper()
            
            with image_placeholder.container():
                st.image(image, caption=f'ISL Sign for "{text.upper()}"', width=300)
            
            # Increment audio key to force new audio element
            st.session_state.tts_audio_key += 1
            st.session_state.tts_current_letter = text.upper()
            
            # Use gTTS to speak the letter with fresh audio in selected language
            try:
                from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_letter_pronunciation
                if is_gtts_available():
                    # Get pronunciation in selected language
                    lang = st.session_state.tts_language
                    pronunciation_text = get_letter_pronunciation(text.upper(), lang)
                    
                    # Clear previous audio and create new
                    with audio_placeholder.container():
                        st.markdown(f"#### 🔊 Audio Pronunciation ({lang.upper()})")
                        speak_text_gtts_visible(pronunciation_text, lang=lang, autoplay=True)
            except Exception:
                pass  # TTS is optional

# Show previously generated result if exists
elif st.session_state.show_sign_result and st.session_state.current_sign_letter:
    letter = st.session_state.current_sign_letter
    image = load_image(letter.lower() + '.jpg')
    if image:
        with image_placeholder.container():
            st.image(image, caption=f'ISL Sign for "{letter}"', width=300)
        
        # Show audio controls without autoplay for returning to page
        try:
            from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_letter_pronunciation
            if is_gtts_available():
                lang = st.session_state.tts_language
                pronunciation_text = get_letter_pronunciation(letter, lang)
                with audio_placeholder.container():
                    st.markdown(f"#### 🔊 Audio Pronunciation ({lang.upper()})")
                    speak_text_gtts_visible(pronunciation_text, lang=lang, autoplay=False)
        except Exception:
            pass


st.markdown("""
    <h2>How It Works</h2>
    <p>
        When you input a single letter (A-Z) or digit (0-9) into the text box, the system automatically displays the corresponding sign language gesture for that character. You can visualize the gesture and learn the ASL representation for each character in real time.
    </p>
    <h2>How to Use</h2>
    <ul>
        <li>Type a single letter (A-Z) or digit (0-9) into the input field.</li>
        <li>Click the 'Convert' button to see the corresponding sign language gesture for the character.</li>
        <li>The gesture image for the alphabet or digit will appear below the input field, helping you understand the sign language symbol.</li>
    </ul>
    <h2>Important Notes</h2>
    <p>
        - Only single alphabets or digits are supported at a time.
        <br>
        - Ensure the input is a valid letter or digit. Special characters or numbers outside the range (A-Z, 0-9) will not be processed.
    </p>
    <h2>Application Scenarios</h2>
    <p>
        This tool is especially useful for learning the fundamentals of American Sign Language, enabling individuals to start by understanding how to sign basic characters. It can also be used in educational settings for teaching young students sign language in a fun and engaging way.
    </p>
""", unsafe_allow_html=True)

     



