import streamlit as st
import speech_recognition as sr
import re  # Regular expression for filtering alphabets
import os

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
    
    Args:
        file_name (str): Name of the file to find (e.g., "a.jpg")
        
    Returns:
        str: Absolute path to the image if found, else None.
    """
    
    folder_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

    image = os.path.join(folder_path, file_name)
    if os.path.exists(image):
        return image
    else:
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