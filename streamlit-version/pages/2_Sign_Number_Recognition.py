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
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings('ignore', category=InconsistentVersionWarning)
except ImportError:
    pass

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.webrtc_utils import RTC_CONFIGURATION, MEDIA_STREAM_CONSTRAINTS
from utils.browser_tts import speak_text
# Import event loop manager to suppress aioice warnings and configure event loop
import utils.event_loop_manager
import logging

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.5

_selected_model = 'standard'

# Initialize session state
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = 'standard'
if 'last_spoken_number' not in st.session_state:
    st.session_state.last_spoken_number = None

st.set_page_config(page_title="Real-Time Sign Number Detection", page_icon="🖐️", layout="wide")

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
num_model = None
try:
    model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'mlp_model_num.p')
    with open(model_path, 'rb') as f:
        model_dict = pickle.load(f)
    num_model = model_dict['model']
    logger.info(f"Loaded num_model: {type(num_model).__name__}, classes: {getattr(num_model, 'classes_', 'N/A')}")
except Exception as e:
    logger.error(f"Failed to load mlp_model_num.p: {e}")
    st.error(f"Failed to load number model: {e}")

# Try to load advanced H5 model if available
model_h5 = None
model_h5_available = False
h5_input_features = None
h5_num_classes = None
h5_labels_dict = None
try:
    import tensorflow as tf
    h5_model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'sign_language_recognition.h5')
    if os.path.exists(h5_model_path):
        model_h5 = tf.keras.models.load_model(h5_model_path)
        h5_input_shape = model_h5.input_shape
        h5_output_shape = model_h5.output_shape
        logger.info(f"H5 model loaded - input: {h5_input_shape}, output: {h5_output_shape}")

        if len(h5_input_shape) == 2 and h5_input_shape[1] is not None:
            h5_input_features = h5_input_shape[1]
            h5_num_classes = h5_output_shape[1] if len(h5_output_shape) == 2 else None
            if h5_num_classes == 10:
                h5_labels_dict = {i: str(i) for i in range(10)}
            elif h5_num_classes == 36:
                h5_labels_dict = {26 + i: str(i) for i in range(10)}
            if h5_labels_dict and h5_input_features == 42:
                model_h5_available = True
                logger.info(f"H5 model compatible for numbers: {h5_input_features} features, {h5_num_classes} classes")
            else:
                logger.warning(f"H5 model shape incompatible for numbers: {h5_input_features} features, {h5_num_classes} classes")
                model_h5_available = False
        else:
            logger.warning(f"H5 model expects non-landmark input: {h5_input_shape}")
            model_h5_available = False
except Exception as e:
    logger.warning(f"H5 model not available: {e}")
    model_h5_available = False

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
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        data_aux = []
        predicted_character = ''
        confidence = 0.0
        
        try:
            detection_results = self.landmarker.detect(mp_image)
        except Exception as e:
            logger.warning(f"Hand detection error: {e}")
            return av.VideoFrame.from_ndarray(img, format="bgr24")
        
        if detection_results.hand_landmarks:
            for hand_landmarks in detection_results.hand_landmarks:
                for landmark in hand_landmarks:
                    x_px = int(landmark.x * W)
                    y_px = int(landmark.y * H)
                    cv2.circle(img, (x_px, y_px), 3, (0, 255, 0), -1)
                
                x_ = [landmark.x for landmark in hand_landmarks]
                y_ = [landmark.y for landmark in hand_landmarks]
                
                for i in range(len(hand_landmarks)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))
            
            # Try H5 model first if selected and compatible
            if (_selected_model == 'advanced' and model_h5_available
                    and model_h5 is not None and h5_input_features == len(data_aux)):
                try:
                    features = np.asarray(data_aux).reshape(1, -1)
                    h5_proba = model_h5.predict(features, verbose=0)
                    max_idx = int(np.argmax(h5_proba[0]))
                    confidence = float(h5_proba[0][max_idx])
                    if confidence >= CONFIDENCE_THRESHOLD and h5_labels_dict:
                        predicted_character = h5_labels_dict.get(max_idx, '')
                    logger.debug(f"H5 number prediction: idx={max_idx} conf={confidence:.2%}")
                except Exception as e:
                    logger.warning(f"H5 prediction failed, falling back to MLP: {e}")
                    predicted_character = ''
                    confidence = 0.0
            
            # MLP model prediction (primary or fallback)
            if not predicted_character and len(data_aux) == 42 and num_model is not None:
                try:
                    features_array = [np.asarray(data_aux)]
                    if hasattr(num_model, 'predict_proba'):
                        proba = num_model.predict_proba(features_array)
                        max_idx = int(np.argmax(proba[0]))
                        confidence = float(proba[0][max_idx])
                        if confidence >= CONFIDENCE_THRESHOLD:
                            predicted_class = num_model.classes_[max_idx]
                            predicted_character = labels_dict.get(int(predicted_class), '')
                        top_indices = np.argsort(proba[0])[::-1][:3]
                        top_preds = [
                            (labels_dict.get(int(num_model.classes_[i]), '?'), f"{proba[0][i]:.0%}")
                            for i in top_indices
                        ]
                        logger.debug(f"Number top-3: {top_preds}")
                    else:
                        prediction = num_model.predict(features_array)
                        predicted_character = labels_dict.get(prediction[0], '')
                        confidence = 1.0
                except Exception as e:
                    logger.warning(f"Number MLP prediction error: {e}")
                    predicted_character = ''
            elif not predicted_character and len(data_aux) != 42:
                logger.debug(f"Number model expects 42 features, got {len(data_aux)}")
            
            if predicted_character:
                self.predicted_number = predicted_character
                
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10
                
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
                display_text = f"{predicted_character} ({confidence:.0%})"
                cv2.putText(img, display_text, (x1, y1 - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
                current_time = time.time()
                if (predicted_character != self.last_spoken and 
                    current_time - self.last_speech_time > self.speech_cooldown):
                    self.last_spoken = predicted_character
                    self.last_speech_time = current_time
            elif confidence > 0 and confidence < CONFIDENCE_THRESHOLD:
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                cv2.putText(img, f"? ({confidence:.0%})", (x1, y1 - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Convert back to av.VideoFrame
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Model selection indicator and Clear button
col_model, col_clear = st.columns([3, 1])
with col_model:
    current_model = st.session_state.get('selected_model', 'standard')
    _selected_model = current_model
    if current_model == 'advanced' and model_h5_available:
        st.success("🧠 Using: **Advanced H5 Model**")
    elif current_model == 'advanced' and not model_h5_available:
        st.warning("⚠️ Advanced model not available, using Standard MLP")
    else:
        st.info(f"🧠 Using: **Standard MLP Model** (confidence threshold: {CONFIDENCE_THRESHOLD:.0%})")

with col_clear:
    if st.button("🗑️ Clear", key="clear_number", help="Clear recognition state and audio cache"):
        st.session_state.pop('last_spoken_number', None)
        st.rerun()

# Create WebRTC context
st.info("📹 Click 'START' to enable camera. Grant browser camera permission when prompted.")
st.markdown("""
    <div style="padding: 10px; background: #2a2a3a; border-radius: 8px; margin-bottom: 15px;">
        <p style="margin: 0; color: #aaa; font-size: 14px;">
            💡 <strong>Tips:</strong> Use Chrome/Edge browser • Allow camera permissions • Ensure stable internet connection
        </p>
    </div>
    """, unsafe_allow_html=True)

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
