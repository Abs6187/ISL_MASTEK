import streamlit as st
import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import warnings
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import time

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*InconsistentVersionWarning.*')

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.webrtc_utils import RTC_CONFIGURATION, MEDIA_STREAM_CONSTRAINTS
from utils.browser_tts import speak_text

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
        .prediction-box {
            background: linear-gradient(145deg, #1E1E1E 0%, #262730 100%);
            border: 2px solid #00BCD4;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        .prediction-text {
            font-size: 48px;
            font-weight: bold;
            color: #4FC3F7;
        }
    </style>
    <h1 style="text-align: center;">🖐️ Real-Time Sign Alphabet to Speech Translation</h1>
    <p style="text-align: center;">
        Using browser camera via WebRTC - works in cloud deployment!
    </p>
    """, unsafe_allow_html=True)

# Load pre-trained models
model_path_42 = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_1.p')
model_42_dict = pickle.load(open(model_path_42, 'rb'))
model_42 = model_42_dict['model']

model_path_84 = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_2.p')
model_84_dict = pickle.load(open(model_path_84, 'rb'))
model_84 = model_84_dict['model']

# Initialize MediaPipe Hands (handle both old and new API versions)
try:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
except AttributeError:
    # Newer MediaPipe versions - solutions still works but may show warnings
    import mediapipe.python.solutions.hands as mp_hands
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

# Labels dictionaries
labels_dict_42 = {0: 'C', 1: 'I', 2: 'L', 3: 'O', 4: 'U', 5: 'V'}
labels_dict_84 = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N', 11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z'}


class SignAlphabetProcessor(VideoProcessorBase):
    """
    VideoProcessor for Sign Alphabet Recognition using WebRTC
    Processes frames from browser camera in real-time
    """
    
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.5
        )
        self.predicted_character = ""
        self.last_spoken = None
        self.last_speech_time = 0
        self.speech_cooldown = 1.5
    
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """
        Process each video frame from browser camera
        
        Args:
            frame: Video frame from browser
            
        Returns:
            Processed frame with hand landmarks and predictions
        """
        # Convert to numpy array
        img = frame.to_ndarray(format="bgr24")
        
        # Flip for mirror effect
        img = cv2.flip(img, 1)
        
        H, W, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(img_rgb)
        
        data_aux = []
        predicted_character = ''
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    img, hand_landmarks,
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
            
            if predicted_character and predicted_character != 'Unknown':
                self.predicted_character = predicted_character
                
                # Draw prediction on frame
                x1, y1 = int(min(x_) * W) - 10, int(min(y_) * H) - 10
                cv2.putText(img, predicted_character, (x1, y1 - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
                # Speak if new character (with cooldown)
                current_time = time.time()
                if (predicted_character != self.last_spoken and 
                    current_time - self.last_speech_time > self.speech_cooldown):
                    self.last_spoken = predicted_character
                    self.last_speech_time = current_time
                    # Note: Browser TTS will be called from main thread
        
        # Convert back to av.VideoFrame
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Create WebRTC context
st.info("📹 Click 'START' to enable camera. Grant browser camera permission when prompted.")

webrtc_ctx = webrtc_streamer(
    key="sign-alphabet-recognition",
    video_processor_factory=SignAlphabetProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints=MEDIA_STREAM_CONSTRAINTS,
    async_processing=True,
)

# Display prediction outside video
st.markdown("### Recognition Output")
col1, col2 = st.columns([2, 1])

with col1:
    prediction_placeholder = st.empty()
    
    if webrtc_ctx.video_processor:
        if webrtc_ctx.video_processor.predicted_character:
            prediction_placeholder.markdown(
                f'<div class="prediction-box"><div class="prediction-text">{webrtc_ctx.video_processor.predicted_character}</div></div>',
                unsafe_allow_html=True
            )
            
            # Browser TTS (executed in main thread)
            if (webrtc_ctx.video_processor.predicted_character != 
                st.session_state.get('last_spoken_char')):
                speak_text(webrtc_ctx.video_processor.predicted_character)
                st.session_state.last_spoken_char = webrtc_ctx.video_processor.predicted_character
        else:
            prediction_placeholder.markdown(
                '<div class="prediction-box"><div class="prediction-text">Waiting for hand...</div></div>',
                unsafe_allow_html=True
            )

with col2:
    st.markdown("**Status:**")
    if webrtc_ctx.state.playing:
        st.success("🟢 Camera Active")
    else:
        st.warning("⚪ Camera Inactive")

st.markdown("""
    <h2>How It Works</h2>
    <p>
        This system uses your browser's camera via WebRTC to detect hand gestures. MediaPipe tracks hand landmarks,
        and our ML model recognizes ISL alphabets in real-time. Audio feedback uses browser's native text-to-speech.
    </p>
    <h2>How to Use</h2>
    <ul>
        <li>Click 'START' and allow camera access when prompted</li>
        <li>Position your hand in the camera view</li>
        <li>Form ISL alphabet signs with your hand</li>
        <li>The system recognizes and speaks the letter</li>
        <li>Works in cloud deployment! No server camera needed.</li>
    </ul>
    <h2>Troubleshooting</h2>
    <p>
        <strong>Camera not working?</strong> Check browser permissions. <br>
        <strong>Black screen?</strong> Ensure you're on HTTPS or localhost. <br>
        <strong>Slow recognition?</strong> Ensure good lighting and clear hand visibility.
    </p>
""", unsafe_allow_html=True)
