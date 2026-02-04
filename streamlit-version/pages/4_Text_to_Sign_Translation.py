import streamlit as st
import os
import sys

# Add parent directory to path for utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

st.set_page_config(page_title="Text to Sign Language", page_icon="📝", layout="wide")

# Initialize session state for audio tracking
if 'tts_current_letter' not in st.session_state:
    st.session_state.tts_current_letter = None
if 'tts_audio_key' not in st.session_state:
    st.session_state.tts_audio_key = 0

# Material UI Color Schema
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

# Create a placeholder for audio that will be cleared on each generation
audio_placeholder = st.empty()

if st.button('Generate Image'):
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
            st.image(image, caption='Generated Image', width=300)
            
            # Increment audio key to force new audio element
            st.session_state.tts_audio_key += 1
            st.session_state.tts_current_letter = text.upper()
            
            # Use gTTS to speak the letter with fresh audio
            try:
                from utils.browser_tts import speak_text_gtts_visible, is_gtts_available
                if is_gtts_available():
                    # Clear previous audio and create new
                    with audio_placeholder.container():
                        st.markdown("#### 🔊 Audio Pronunciation")
                        speak_text_gtts_visible(f"The letter {text.upper()}", autoplay=True)
            except Exception:
                pass  # TTS is optional


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

     



