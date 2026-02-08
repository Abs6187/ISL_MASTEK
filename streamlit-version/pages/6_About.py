import streamlit as st

# Set dark theme
st.set_page_config(page_title="About the Application", page_icon="ℹ️", layout="wide")

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
            p {
                font-size: 18px;
                color: #E0E0E0;
                line-height: 1.7;
            }
            h1 {
                background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 50%, #00BCD4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            h2 {
                color: #00BCD4;
                font-weight: 600;
            }
            ul, li {
                color: #E0E0E0;
                font-size: 18px;
                line-height: 1.8;
            }
            strong {
                color: #4FC3F7;
                font-weight: 600;
            }
    </style>
    <h1 style="text-align: center; color: white;">About the Application</h1>
    <p style="text-align: center; color: white; font-size: 18px;">
        This application aims to bridge communication gaps between hearing and non-hearing individuals by providing real-time sign language recognition. The app supports both text-to-sign and speech-to-sign functionalities for seamless communication. It includes features for converting spoken words or text into corresponding Indian Sign Language (ISL) gestures, displayed as images or animations. It allows individuals to communicate effectively, understand, and learn sign language.
    </p>

    <h2 style="color: white;">🛠 Features:</h2>
    <ul style="color: white; font-size: 18px">
        <li><strong>Speech to Sign Language:</strong> Converts spoken words into sign language gestures for individual alphabets and numbers.</li>
        <li><strong>Text to Sign Language:</strong> Converts typed text (alphabets and numbers) into corresponding sign language gestures.</li>
        <li><strong>Real-time Translation:</strong> Instant sign language gestures based on speech or text input.</li>
        <li><strong>Multi-language Support:</strong> Can be expanded to support other sign language systems.</li>
        <li><strong>User-Friendly Interface:</strong> Simple and easy-to-use interface with live sign language images.</li>
    </ul>

    <h2 style="color: white;">💻 Technologies Used:</h2>
    <ul style="color: white; font-size: 18px">
        <li><strong>Streamlit:</strong> For building the interactive user interface.</li>
        <li><strong>SpeechRecognition API:</strong> For converting speech to text.</li>
        <li><strong>gTTS (Google Text-to-Speech):</strong> For adding voice features.</li>
        <li><strong>OpenCV, TensorFlow/Keras:</strong> For real-time sign language gesture detection using trained models.</li>
        <li><strong>Python:</strong> For backend and logic development.</li>
        <li><strong>HTML/CSS:</strong> For custom page designs.</li>
    </ul>

    <h2 style="color: white;">🌍 Purpose and Impact:</h2>
    <p style="color: white; font-size: 18px;">
        This application is designed to enhance accessibility and inclusivity for the deaf and hard-of-hearing community. By converting speech or text into sign language gestures, it promotes equal communication opportunities. It is also a valuable educational tool for individuals learning sign language.
    </p>

    <h2 style="color: white;">📚 How to Use:</h2>
    <ul style="color: white; font-size: 18px">
        <li><strong>Live Gesture Recognition:</strong> Use your camera to translate real-time sign language gestures into text and speech.</li>
        <li><strong>Speech to Sign Language:</strong> Speak out a word or letter clearly, and the app will convert it into the corresponding sign language gesture.</li>
        <li><strong>Text to Sign Language:</strong> Type in a word or letter, and the app will display the sign language gesture for it.</li>
    </ul>
""", unsafe_allow_html=True)
