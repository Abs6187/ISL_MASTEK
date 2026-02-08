import streamlit as st
import re  # Regular expression for filtering alphabets
import os
import streamlit.components.v1 as components

# Try to import speech_recognition (not available in cloud)
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Initialize session state for detected letter and audio tracking
if 'detected_letter' not in st.session_state:
    st.session_state.detected_letter = None
if 'speech_audio_key' not in st.session_state:
    st.session_state.speech_audio_key = 0
if 'last_spoken_letter' not in st.session_state:
    st.session_state.last_spoken_letter = None
if 'speech_tts_language' not in st.session_state:
    st.session_state.speech_tts_language = "en"

st.set_page_config(page_title="Speech to Sign Language ", page_icon="🎙️", layout="wide")

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
    <h1 style="text-align: center;">Speech to Sign Language (Single Alphabet)</h1>
    <h6 style="text-align: center;">
        This feature converts a single alphabet or digit spoken by the user into its corresponding Indian Sign Language (ISL) gesture representation.
    </h6>
    """, unsafe_allow_html=True)


def load_image(file_name):
    """
    Searches for an image file in the 'assets/images' directory.
    Uses case-insensitive matching to handle mixed case filenames.
    
    Args:
        file_name (str): Name of the file to find (e.g., "a.jpg")
        
    Returns:
        str: Absolute path to the image if found, else None.
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

# Language selection for audio pronunciation (shown for both cloud and local)
st.markdown("### 🌐 Language Settings")
try:
    from utils.browser_tts import get_indian_languages, is_gtts_available
    if is_gtts_available():
        languages = get_indian_languages()
        selected_lang_name = st.selectbox(
            "Select language for audio pronunciation:",
            list(languages.keys()),
            index=0,
            key="speech_lang_selector"
        )
        st.session_state.speech_tts_language = languages[selected_lang_name]
    else:
        st.info("gTTS not available - audio will use English")
except ImportError:
    st.info("Language module not available")

st.markdown("---")

# Check if speech recognition is available
if not SPEECH_RECOGNITION_AVAILABLE:
    st.info("🌐 **Using Browser-Based Speech Recognition** (Cloud Compatible)")
    st.markdown("""
        <style>
            .speech-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .speech-btn {
                background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
                color: #FAFAFA;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px 5px;
                transition: all 0.3s ease;
            }
            .speech-btn:hover {
                background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
                transform: translateY(-1px);
            }
            .speech-btn:disabled {
                background: #666;
                cursor: not-allowed;
            }
            #status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-align: center;
            }
            .status-listening {
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
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎤 Browser Speech Recognition")
    st.write("Enter a letter manually or use browser speech recognition below.")
    
    # Manual input fallback - always works
    col1, col2 = st.columns([3, 1])
    with col1:
        manual_letter = st.text_input("Enter a letter (A-Z):", max_chars=1, key="manual_letter").upper()
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        show_manual = st.button("Show Sign", key="show_manual")
    
    if show_manual and manual_letter:
        if manual_letter.isalpha():
            # Only update if letter changed to prevent audio caching issues
            if st.session_state.detected_letter != manual_letter:
                st.session_state.detected_letter = manual_letter
                st.session_state.speech_audio_key += 1
                st.session_state.last_spoken_letter = None  # Reset to allow new audio
        else:
            st.warning("Please enter a valid letter (A-Z)")
    
    # Browser speech recognition using Streamlit component
    st.markdown("---")
    st.markdown("### 🎙️ Or Use Voice Recognition")
    st.write("Click the button and say 'Letter A' (or any letter A-Z)")
    
    # JavaScript-based speech recognition that updates a hidden input
    speech_html = """
    <style>
        .speech-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .speech-btn {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
            color: #FAFAFA;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        .speech-btn:hover {
            background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
            transform: translateY(-1px);
        }
        .speech-btn:disabled {
            background: #666;
            cursor: not-allowed;
        }
        #status {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            text-align: center;
        }
        .status-listening {
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
    </style>
    <div class="speech-container">
        <div id="status" class="status-info">Ready to listen...</div>
        
        <div style="text-align: center; margin: 15px 0;">
            <button class="speech-btn" id="start-btn" onclick="startListening()">🎤 Start Listening</button>
            <button class="speech-btn" id="stop-btn" onclick="stopListening()" disabled>⏹️ Stop</button>
        </div>
        
        <div id="result-text" style="text-align: center; font-size: 18px; color: #E0E0E0; margin: 15px 0;"></div>
        <div id="detected-letter" style="text-align: center; font-size: 48px; font-weight: bold; color: #00BCD4; margin: 15px 0;"></div>
    </div>
    
    <script>
        let recognition;
        let isListening = false;
        
        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isListening = true;
                document.getElementById('status').className = 'status-listening';
                document.getElementById('status').textContent = '🎤 Listening... Say "Letter A" or similar';
                document.getElementById('start-btn').disabled = true;
                document.getElementById('stop-btn').disabled = false;
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('result-text').textContent = 'You said: "' + transcript + '"';
                
                // Extract letter - match "letter X" or just single letters
                let letter = null;
                const letterMatch = transcript.toLowerCase().match(/letter\\s*([a-z])/i);
                if (letterMatch) {
                    letter = letterMatch[1].toUpperCase();
                } else {
                    // Try to find any single letter
                    const singleMatch = transcript.trim().match(/^([a-z])$/i);
                    if (singleMatch) {
                        letter = singleMatch[1].toUpperCase();
                    }
                }
                
                if (letter) {
                    document.getElementById('status').className = 'status-info';
                    document.getElementById('status').textContent = '✅ Detected letter: ' + letter + ' - Click "Use This Letter" below!';
                    document.getElementById('detected-letter').textContent = letter;
                    
                    // Store in localStorage for Streamlit to read
                    localStorage.setItem('detected_letter', letter);
                } else {
                    document.getElementById('status').className = 'status-error';
                    document.getElementById('status').textContent = '❌ No letter detected. Please say "Letter" followed by A-Z';
                }
            };
            
            recognition.onerror = function(event) {
                document.getElementById('status').className = 'status-error';
                document.getElementById('status').textContent = '❌ Error: ' + event.error;
                resetButtons();
            };
            
            recognition.onend = function() {
                resetButtons();
            };
        } else {
            document.getElementById('status').className = 'status-error';
            document.getElementById('status').textContent = '❌ Speech recognition not supported. Use manual input above or try Chrome/Edge.';
            document.getElementById('start-btn').disabled = true;
        }
        
        function startListening() {
            if (recognition && !isListening) {
                recognition.start();
            }
        }
        
        function stopListening() {
            if (recognition && isListening) {
                recognition.stop();
            }
        }
        
        function resetButtons() {
            isListening = false;
            document.getElementById('start-btn').disabled = false;
            document.getElementById('stop-btn').disabled = true;
            if (document.getElementById('status').className === 'status-listening') {
                document.getElementById('status').className = 'status-info';
                document.getElementById('status').textContent = 'Ready to listen...';
            }
        }
    </script>
    """
    
    components.html(speech_html, height=250)
    
    # Streamlit button to use the detected letter
    voice_letter = st.text_input("Detected letter (copy from above or type):", key="voice_letter", max_chars=1).upper()
    if st.button("Use This Letter", key="use_voice") and voice_letter:
        if voice_letter.isalpha():
            # Only update if letter changed to prevent audio caching issues
            if st.session_state.detected_letter != voice_letter:
                st.session_state.detected_letter = voice_letter
                st.session_state.speech_audio_key += 1
                st.session_state.last_spoken_letter = None  # Reset to allow new audio
        else:
            st.warning("Please enter a valid letter (A-Z)")
    
    # Display the sign image if a letter was detected
    if st.session_state.detected_letter:
        st.markdown("---")
        st.markdown(f"### Sign for Letter: {st.session_state.detected_letter}")
        
        image_path = load_image(st.session_state.detected_letter + '.jpg')
        if image_path:
            st.image(image_path, caption=f'ISL Sign for "{st.session_state.detected_letter}"', width=300)
            
            # Use gTTS to speak the letter in selected language - only if it's a new letter
            current_letter = st.session_state.detected_letter
            lang = st.session_state.speech_tts_language
            
            if st.session_state.last_spoken_letter != current_letter:
                try:
                    from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_letter_pronunciation
                    if is_gtts_available():
                        pronunciation_text = get_letter_pronunciation(current_letter, lang)
                        st.markdown(f"#### 🔊 Audio Pronunciation ({lang.upper()})")
                        speak_text_gtts_visible(pronunciation_text, lang=lang, autoplay=True)
                        st.session_state.last_spoken_letter = current_letter
                except Exception as e:
                    pass  # TTS is optional
            else:
                # Show audio controls without autoplay for repeat plays
                try:
                    from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_letter_pronunciation
                    if is_gtts_available():
                        pronunciation_text = get_letter_pronunciation(current_letter, lang)
                        st.markdown(f"#### 🔊 Audio Pronunciation ({lang.upper()})")
                        speak_text_gtts_visible(pronunciation_text, lang=lang, autoplay=False)
                except Exception:
                    pass
        else:
            st.error(f'Image for letter "{st.session_state.detected_letter}" not found.')
        
        # Clear button with better styling
        st.markdown("---")
        if st.button("🗑️ Clear All & Reset", key="clear_letter", use_container_width=True):
            st.session_state.detected_letter = None
            st.session_state.last_spoken_letter = None
            st.session_state.speech_audio_key += 1
            st.rerun()
    
    st.stop()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Placeholder for error messages
error_placeholder = st.empty()

# Function to listen to speech and convert to text (only alphabets)
def listen_for_alphabets():
    """
    Listens for speech input, recognizes text using Google Speech Recognition,
    and filters for alphabets only.
    
    Returns:
        str: The recognized alphabetic characters string (A-Z).
        
    Example:
        User speaks: "Letter A" -> functions detects "Letter A" -> returns "A"
    """
    with sr.Microphone() as source:
        st.info("Listening for alphabets... Please speak!")
        audio = recognizer.listen(source, timeout=5)
        try:
            # Recognize speech using Google's speech recognition API
            text = recognizer.recognize_google(audio)
            
            # Filter out non-alphabet characters using regex (A-Z, case insensitive)
            alphabets_only = re.sub(r'[^a-zA-Z]', '', text)
            
            # Show only alphabets in the result
            if alphabets_only:
                st.success(f"Recognized Text (Alphabets Only): {alphabets_only}")
            else:
                st.warning("No valid alphabetic characters detected.")
            return alphabets_only
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the speech.")
            return ""
        except sr.RequestError:
            st.error("Sorry, there was an issue with the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            st.warning("No speech detected within the timeout period.")
            return ""
        
def load_image_native(file_name):
    """
    Searches for an image file in the 'assets/images' directory.
    Uses case-insensitive matching to handle mixed case filenames.
    
    Args:
        file_name (str): Name of the file to find (e.g., "a.jpg")
        
    Returns:
        str: Absolute path to the image if found, else None.
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


st.header("Listen for Alphabets")

try:
    # Button to trigger speech recognition
    if st.button("Listen"):
        recognized_text = listen_for_alphabets()

        recognized_text = recognized_text.lower()
        # Use regular expression to extract the letter
        match = re.search(r'letter([A-Za-z])', recognized_text)

        if match:
            recognized_text = match.group(1)
            st.write("Recognized Text:", recognized_text.upper())

        else:
            recognized_text = ''
            st.write("No valid alphabet detected.")



        # Load the image
        if recognized_text == '':
            st.write('Please enter some text.')
        elif len(recognized_text.split()) > 1:
            st.write('Please enter only one word.')

        elif recognized_text.isalpha() == False and recognized_text.isdigit() == False:
            st.write('Please enter only alphabets or numbers.')

        else:
            st.write('Generating image...')

            # Load the image
            image = load_image_native(recognized_text + '.jpg')
            if image is None:
                st.write('Image not found. Please try again.')
            else:
                st.image(image, caption='Generated Image', width=300)
                
                # Increment audio key to force fresh audio
                st.session_state.speech_audio_key += 1
                
                # Use gTTS to speak the letter with fresh audio in selected language
                try:
                    from utils.browser_tts import speak_text_gtts_visible, is_gtts_available, get_letter_pronunciation
                    if is_gtts_available():
                        lang = st.session_state.speech_tts_language
                        pronunciation_text = get_letter_pronunciation(recognized_text.upper(), lang)
                        st.markdown(f"#### 🔊 Audio Pronunciation ({lang.upper()})")
                        speak_text_gtts_visible(pronunciation_text, lang=lang, autoplay=True)
                except Exception:
                    pass  # TTS is optional
        
except Exception as e:
     error_placeholder.error("An error occurred. Please try again.")

# Explanation and usage
st.markdown("""
    <h2>How It Works</h2>
    <p>
        This tool listens for spoken alphabets (A-Z). Once you speak, it identifies the character and shows its corresponding Indian Sign Language gesture. It can assist in learning and practicing sign language gestures in real-time.
    </p>
    <h2>How to Use</h2>
    <ul>
        <li>Click on the 'Start Listening' button.</li>
        <li>Speak "Letter" followed by a single letter (A-Z) clearly.</li>
        <li>The system will show the corresponding sign language gesture for that character.</li>
    </ul>
    <h2>Important Notes</h2>
    <p>
        - Only single letters (A-Z) are supported at a time.
        <br>
        - Make sure your pronunciation is clear for better recognition.
        <br>
        - Ensure the input is a valid alphabet or digit. Other characters will not be processed.
    </p>
    <h2>Application Scenarios</h2>
    <p>
        This tool is ideal for learning the basics of Indian Sign Language (ISL). It helps beginners understand and practice signing individual letters or digits. It can also be helpful in educational settings for teaching young learners or as a starting point for anyone interested in learning ISL.
    </p>
""", unsafe_allow_html=True)