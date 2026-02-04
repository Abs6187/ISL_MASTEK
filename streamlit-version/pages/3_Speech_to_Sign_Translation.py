import streamlit as st
import re  # Regular expression for filtering alphabets
import os

# Try to import speech_recognition (not available in cloud)
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

st.set_page_config(page_title="Speech to Sign Language ", page_icon="🎙️", layout="wide")

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
    <h1 style="text-align: center;">Speech to Sign Language (Single Alphabet)</h1>
    <h6 style="text-align: center;">
        This feature converts a single alphabet or digit spoken by the user into its corresponding Indian Sign Language (ISL) gesture representation.
    </h6>
    """, unsafe_allow_html=True)


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
            #speech-text {
                width: 100%;
                min-height: 100px;
                padding: 15px;
                font-size: 16px;
                background: #1E1E1E;
                color: #E0E0E0;
                border: 2px solid #00BCD4;
                border-radius: 8px;
                margin: 20px 0;
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
            #result-image {
                max-width: 300px;
                margin: 20px auto;
                display: block;
            }
        </style>
        
        <div class="speech-container">
            <h2 style="color: #00BCD4; text-align: center;">🎤 Browser Speech Recognition (Cloud Compatible)</h2>
            <p style="text-align: center; color: #E0E0E0;">Click "Start Listening" and say "Letter" followed by an alphabet (A-Z)</p>
            
            <div id="status" class="status-info">Ready to listen...</div>
            
            <div style="text-align: center;">
                <button class="speech-btn" id="start-btn" onclick="startListening()">🎤 Start Listening</button>
                <button class="speech-btn" id="stop-btn" onclick="stopListening()" disabled>⏹️ Stop</button>
            </div>
            
            <textarea id="speech-text" placeholder="Speech will appear here..." readonly></textarea>
            
            <div id="result-container" style="text-align: center;">
                <img id="result-image" style="display:none;" />
            </div>
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
                    document.getElementById('speech-text').value = 'You said: ' + transcript;
                    
                    // Extract letter
                    const match = transcript.toLowerCase().match(/letter\s*([a-z])/);
                    if (match) {
                        const letter = match[1].toUpperCase();
                        document.getElementById('status').className = 'status-info';
                        document.getElementById('status').textContent = '✅ Detected:  ' + letter;
                        
                        // Try to load the image
                        const img = document.getElementById('result-image');
                        img.style.display = 'block';
                        img.alt = 'Sign for ' + letter;
                        
                        // You would replace this with actual image paths
                        img.onerror = function() {
                            document.getElementById('status').className = 'status-error';
                            document.getElementById('status').textContent = '⚠️ Image for "' + letter + '" not found';
                        };
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
                document.getElementById('status').textContent = '❌ Speech recognition not supported in this browser. Try Chrome or Edge.';
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
    """, unsafe_allow_html=True)
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
            image = load_image(recognized_text + '.jpg')
            if image is None:
                st.write('Image not found. Please try again.')
            else:
                st.image(image, caption='Generated Image', width=300)
        
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