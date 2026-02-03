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
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*InconsistentVersionWarning.*')

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.webrtc_utils import RTC_CONFIGURATION, MEDIA_STREAM_CONSTRAINTS
from utils.browser_tts import speak_text
# Import event loop manager to suppress aioice warnings and configure event loop
import utils.event_loop_manager

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
    <h1 style="text-align: center;">🖐️ Real-Time Sign Number to Speech Translation</h1>
    <p style="text-align: center;">
        Using browser camera via WebRTC - works in cloud deployment!
    </p>
    """, unsafe_allow_html=True)

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_num.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

# Initialize MediaPipe Tasks Hand Landmarker
model_path_task = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'hand_landmarker.task')
base_options = python.BaseOptions(model_asset_path=model_path_task)
hand_landmarker_options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.3,
    min_hand_presence_confidence=0.3
)

# Labels dictionary for gestures
labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '0'}


class SignNumberProcessor(VideoProcessorBase):
    """
    VideoProcessor for Sign Number Recognition using WebRTC
    Processes frames from browser camera in real-time
    """
    
    def __init__(self):
        self.landmarker = vision.HandLandmarker.create_from_options(hand_landmarker_options)
        self.predicted_number = ""
        self.last_spoken = None
        self.last_speech_time = 0
        self.speech_cooldown = 1.5
    
    def __del__(self):
        """Cleanup MediaPipe resources when processor is destroyed"""
        try:
            if hasattr(self, 'landmarker') and self.landmarker:
                self.landmarker.close()
        except Exception:
            # Ignore cleanup errors - they're non-critical
            pass
    
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
        
        # Process with MediaPipe Tasks API
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        results = self.landmarker.detect(mp_image)
        
        data_aux = []
        predicted_character = 'Unknown'
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                # Draw landmarks manually with cv2
                for landmark in hand_landmarks:
                    x_px = int(landmark.x * W)
                    y_px = int(landmark.y * H)
                    cv2.circle(img, (x_px, y_px), 3, (0, 255, 0), -1)
                
                # Extract and normalize landmarks
                x_ = [landmark.x for landmark in hand_landmarks]
                y_ = [landmark.y for landmark in hand_landmarks]
                
                for i in range(len(hand_landmarks)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))
            
            # Predict if we have correct feature count
            if len(data_aux) == 42:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict.get(prediction[0], 'Unknown')
                
                if predicted_character != 'Unknown':
                    self.predicted_number = predicted_character
                    
                    # Draw bounding box and label
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10
                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
                    cv2.putText(img, predicted_character, (x1, y1 - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                    
                    # Track for speech (will be called from main thread)
                    current_time = time.time()
                    if (predicted_character != self.last_spoken and 
                        current_time - self.last_speech_time > self.speech_cooldown):
                        self.last_spoken = predicted_character
                        self.last_speech_time = current_time
        
        # Convert back to av.VideoFrame
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Create WebRTC context
st.info("📹 Click 'START' to enable camera. Grant browser camera permission when prompted.")

webrtc_ctx = webrtc_streamer(
    key="sign-number-recognition",
    video_processor_factory=SignNumberProcessor,
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
        if webrtc_ctx.video_processor.predicted_number:
            prediction_placeholder.markdown(
                f'<div class="prediction-box"><div class="prediction-text">{webrtc_ctx.video_processor.predicted_number}</div></div>',
                unsafe_allow_html=True
            )
            
            # Browser TTS (executed in main thread)
            if (webrtc_ctx.video_processor.predicted_number != 
                st.session_state.get('last_spoken_number')):
                speak_text(webrtc_ctx.video_processor.predicted_number)
                st.session_state.last_spoken_number = webrtc_ctx.video_processor.predicted_number
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
        The system uses your browser's camera to detect hand gestures for numbers 0-9. MediaPipe tracks hand landmarks,
        and our ML model recognizes ISL numbers in real-time. Audio uses browser's text-to-speech.
    </p>
    <h2>How to Use</h2>
    <ul>
        <li>Click 'START' and allow camera access</li>
        <li>Position your hand in view</li>
        <li>Form ISL number signs (0-9)</li>
        <li>System recognizes and speaks the number</li>
        <li>Fully cloud-compatible!</li>
    </ul>
    <h2>Troubleshooting</h2>
    <p>
        <strong>Camera not working?</strong> Check browser permissions. <br>
        <strong>Black screen?</strong> Use HTTPS or localhost. <br>
        <strong>Slow?</strong> Ensure good lighting and clear hand visibility.
    </p>
""", unsafe_allow_html=True)
