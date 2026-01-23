import streamlit as st
import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
import time
from gtts import gTTS
from io import BytesIO
import pygame

st.set_page_config(page_title="Real-Time Sign Alphabet Detection", page_icon="🖐️", layout="wide")

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
        }
        h2 {
            color: #00BCD4;
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
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
            transform: translateY(-1px);
        }
    </style>
    <h1 style="text-align: center;">🖐️ Real-Time Sign Alphabet to Speech Translation</h1>
    <p style="text-align: center;">
        This feature translates indian sign language(ISL) alphabets into speech in real-time, helping non-signers understand numeric gestures made by the user.
    </p>
    """, unsafe_allow_html=True)

run = st.checkbox("Start Camera")

# Initialize pygame mixer for non-blocking audio playback
pygame.mixer.init()

# Load pre-trained models
model_path_42 = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_1.p')
model_42_dict = pickle.load(open(model_path_42, 'rb'))
model_42 = model_42_dict['model']

model_path_84 = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_2.p')
model_84_dict = pickle.load(open(model_path_84, 'rb'))
model_84 = model_84_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3, min_tracking_confidence=0.5)

# Labels dictionaries
labels_dict_42 = {0: 'C', 1: 'I', 2: 'L', 3: 'O', 4: 'U', 5: 'V'}
labels_dict_84 = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N', 11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z'}

# Function to play text as speech asynchronously
def speak(text):
    """
    Converts text to speech using Google Text-to-Speech (gTTS) and plays it.

    Args:
        text (str): The text to be spoken.
        
    Example:
        speak("A")  # Plays audio "A"
    """
    if text:
        tts = gTTS(text=text, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        # Play audio using pygame (non-blocking)
        pygame.mixer.music.load(audio_fp, "mp3")
        pygame.mixer.music.play()

# Placeholder for video frame
frame_window = st.empty()

# Track last spoken letter and cooldown timer
last_spoken = None
last_speech_time = 0
speech_cooldown = 1.5  # Wait time before speaking again


# Start video processing
if run:
    st.write("Starting Gesture Recognition...")

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        data_aux = []
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        predicted_character = ''

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                # Extract landmarks
                x_ = [landmark.x for landmark in hand_landmarks.landmark]
                y_ = [landmark.y for landmark in hand_landmarks.landmark]

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))

            # Model prediction
            if len(data_aux) == 42:
                prediction = model_42.predict([np.asarray(data_aux)])
                predicted_character = labels_dict_42.get(prediction[0], 'Unknown')
            elif len(data_aux) == 84:
                prediction = model_84.predict([np.asarray(data_aux)])
                predicted_character = labels_dict_84.get(prediction[0], 'Unknown')

            # Draw prediction on the frame
            x1, y1 = int(min(x_) * W) - 10, int(min(y_) * H) - 10
            cv2.putText(frame, predicted_character, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

            # Speak only if it's a new character and cooldown has passed
            current_time = time.time()
            if predicted_character != last_spoken and predicted_character != 'Unknown' and (current_time - last_speech_time > speech_cooldown):
                speak(predicted_character)
                last_spoken = predicted_character
                last_speech_time = current_time

        # Display the frame in Streamlit
        frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Stop if checkbox is unchecked
        if not run:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    st.write("Video Stream Stopped")

st.markdown("""
    <h2>How It Works</h2>
    <p>
        The system uses your camera to detect hand gestures corresponding to numbers. Once a gesture is recognized, it is converted into a spoken word using the gTTS (Google Text-to-Speech) API.
    </p>
    <h2>How to Use</h2>
    <ul>
        <li>Enable the camera by clicking the 'Start Camera' button.</li>
        <li>Position your hand in front of the camera, forming numbers with your fingers.</li>
        <li>The system will automatically recognize the sign number and speak the corresponding number aloud.</li>
    </ul>
    <h2>Troubleshooting</h2>
    <p>
        If the system is not recognizing your hand correctly, make sure it is fully visible and well-lit.
    </p>
""", unsafe_allow_html=True)
