import streamlit as st
import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
import time
import pygame
from io import BytesIO
from gtts import gTTS

st.set_page_config(page_title="Real-Time Sign Number Detection", page_icon="🖐️", layout="wide")

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
    <h1 style="text-align: center;">🖐️ Real-Time Sign Number to Speech Translation</h1>
    <p style="text-align: center;">
        This feature translates sign language numbers into speech in real-time, helping non-signers understand numeric gestures made by user.
    </p>
    """, unsafe_allow_html=True)

run = st.checkbox("Start Camera")


# Initialize pygame mixer for non-blocking audio playback
pygame.mixer.init()

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_num.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3, min_tracking_confidence=0.5)

# Labels dictionary for gestures
labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '0'}

# Function to speak the text
def speak(text):
    if text:
        tts = gTTS(text=text, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        # Play audio using pygame (non-blocking)
        pygame.mixer.music.load(audio_fp, "mp3")
        pygame.mixer.music.play()

# Placeholder for video
frame_placeholder = st.empty()

# Function to play text as speech asynchronously
last_spoken = None  # Track last spoken number to avoid repetition
last_speech_time = 0  # Track last speech time for cooldown
speech_cooldown = 1.5  # Wait time before speaking again




# Start camera and real-time gesture recognition
if run:
    st.write("Starting Hand Gesture Recognition...")

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        data_aux = []
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        H, W, _ = frame.shape

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame for hand landmarks
        results = hands.process(frame_rgb)
        
        predicted_character = 'Unknown'

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                # Extract and normalize landmarks
                x_ = [landmark.x for landmark in hand_landmarks.landmark]
                y_ = [landmark.y for landmark in hand_landmarks.landmark]

                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))

            if len(data_aux) == 42:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict.get(prediction[0], 'Unknown')

                # Draw bounding box and label
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            1.3, (0, 0, 0), 3, cv2.LINE_AA)
                
                current_time = time.time()
                if predicted_character != last_spoken and predicted_character != 'Unknown' and (current_time - last_speech_time > speech_cooldown):
                    speak(predicted_character)
                    last_spoken = predicted_character
                    last_speech_time = current_time

        # Display the frame in Streamlit
        frame_placeholder.image(frame, channels="BGR")        


        # Stop camera when checkbox is unchecked
        if not run:
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    st.write("Camera stopped.")

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
