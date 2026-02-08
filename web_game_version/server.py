import os
import logging
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request
import cv2
import numpy as np
import pickle
import base64
from flask_cors import CORS
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CONFIDENCE_THRESHOLD = 0.5
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
RunningMode = vision.RunningMode


app = Flask(__name__, 
            static_url_path='', 
            static_folder=os.path.join(os.path.dirname(__file__), 'frontend'))
CORS(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')

# Load models and labels
model_42 = None
model_84 = None
math_model = None
labels_dict_42 = {0: 'C', 1: 'I', 2: 'L', 3: 'O', 4: 'U', 5: 'V'}
labels_dict_84 = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N', 11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z'}
math_labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '0'}

try:
    model_path_1 = os.path.join(os.path.dirname(__file__), 'mlp_model_1.p')
    with open(model_path_1, 'rb') as f:
        model_42 = pickle.load(f)['model']
    logger.info(f"Loaded model_42: classes={getattr(model_42, 'classes_', 'N/A')}")
except Exception as e:
    logger.error(f"Failed to load mlp_model_1.p: {e}")

try:
    model_path_2 = os.path.join(os.path.dirname(__file__), 'mlp_model_2.p')
    with open(model_path_2, 'rb') as f:
        model_84 = pickle.load(f)['model']
    logger.info(f"Loaded model_84: classes={getattr(model_84, 'classes_', 'N/A')}")
except Exception as e:
    logger.error(f"Failed to load mlp_model_2.p: {e}")

try:
    model_path_num = os.path.join(os.path.dirname(__file__), 'mlp_model_num.p')
    with open(model_path_num, 'rb') as f:
        math_model = pickle.load(f)['model']
    logger.info(f"Loaded math_model: classes={getattr(math_model, 'classes_', 'N/A')}")
except Exception as e:
    logger.error(f"Failed to load mlp_model_num.p: {e}")

# Initialize MediaPipe Tasks Hand Landmarker
model_path_task = os.path.join(os.path.dirname(__file__), 'models', 'hand_landmarker.task')
base_options = python.BaseOptions(model_asset_path=model_path_task)
options = HandLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.3,
    min_hand_presence_confidence=0.3
)
landmarker = HandLandmarker.create_from_options(options)




@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts the sign language character from an input image.

    Expected JSON Input:
    {
        "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",  # Base64 encoded image string
        "category": "general" or "math"                     # Optional: defaults to 'general'
    }

    Returns:
    {
        "letter": "A"  # The predicted character
    }
    
    Example Usage:
    curl -X POST http://localhost:5000/predict \\
         -H "Content-Type: application/json" \\
         -d '{"image": "data:image/png;base64,..."}'
    """
    try:
        data = request.get_json()
    except Exception as e:
        logger.warning(f"Invalid JSON in request: {e}")
        return jsonify({'letter': '', 'confidence': 0, 'error': 'Invalid JSON'}), 400

    if not data or 'image' not in data:
        return jsonify({'letter': '', 'confidence': 0, 'error': 'No image provided'}), 400

    category = data.get('category', 'general')
    logger.debug(f"Received prediction request, category: {category}")

    # Decode base64 image
    try:
        image_data = data['image'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({'letter': '', 'confidence': 0, 'error': 'Failed to decode image'}), 400
        frame = cv2.flip(frame, 1)
        H, W, _ = frame.shape
    except Exception as e:
        logger.warning(f"Image decode error: {e}")
        return jsonify({'letter': '', 'confidence': 0, 'error': 'Invalid image data'}), 400

    # Process frame with Tasks API
    try:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = landmarker.detect(mp_image)
    except Exception as e:
        logger.warning(f"Hand detection error: {e}")
        return jsonify({'letter': '', 'confidence': 0, 'error': 'Detection failed'}), 500

    predicted_character = ''
    confidence = 0.0

    if results.hand_landmarks:
        data_aux = []
        for hand_landmarks in results.hand_landmarks:
            x_ = [lm.x for lm in hand_landmarks]
            y_ = [lm.y for lm in hand_landmarks]
            
            min_x = min(x_)
            min_y = min(y_)
            for i in range(len(hand_landmarks)):
                data_aux.append(x_[i] - min_x)
                data_aux.append(y_[i] - min_y)

        target_model = None
        target_labels = None

        if category == "math":
            if len(data_aux) == 42 and math_model is not None:
                target_model = math_model
                target_labels = math_labels_dict
        else:
            if len(data_aux) == 42 and model_42 is not None:
                target_model = model_42
                target_labels = labels_dict_42
            elif len(data_aux) == 84 and model_84 is not None:
                target_model = model_84
                target_labels = labels_dict_84

        if target_model is not None and target_labels is not None:
            try:
                features_array = [np.asarray(data_aux)]
                if hasattr(target_model, 'predict_proba'):
                    proba = target_model.predict_proba(features_array)
                    max_idx = int(np.argmax(proba[0]))
                    confidence = float(proba[0][max_idx])
                    if confidence >= CONFIDENCE_THRESHOLD:
                        predicted_class = target_model.classes_[max_idx]
                        predicted_character = target_labels.get(int(predicted_class), '')
                    top_indices = np.argsort(proba[0])[::-1][:3]
                    top_preds = [
                        (target_labels.get(int(target_model.classes_[i]), '?'), f"{proba[0][i]:.0%}")
                        for i in top_indices
                    ]
                    logger.debug(f"Top-3: {top_preds} | cat={category} feat={len(data_aux)} conf={confidence:.2%}")
                else:
                    pred = target_model.predict(features_array)
                    predicted_character = target_labels.get(pred[0], '')
                    confidence = 1.0
            except Exception as e:
                logger.warning(f"Prediction error: {e}")
                predicted_character = ''
        elif len(data_aux) not in (42, 84):
            logger.debug(f"Unexpected feature count: {len(data_aux)}")

    return jsonify({'letter': predicted_character, 'confidence': round(confidence, 3)})

# Initialize PPLX Service
from pplx_service import PPLXService
pplx_service = PPLXService()

@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    word = data.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400
    
    response = pplx_service.get_intelligent_response(word)
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
