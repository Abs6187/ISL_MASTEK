import os
from dotenv import load_dotenv
load_dotenv() # Load env vars from .env file

from flask import Flask, jsonify, request
import cv2
import numpy as np
import pickle
import base64
from flask_cors import CORS
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
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
import os
# Load models and labels
model_path_1 = os.path.join(os.path.dirname(__file__), 'mlp_model_1.p')
model_42 = pickle.load(open(model_path_1, 'rb'))['model']

model_path_2 = os.path.join(os.path.dirname(__file__), 'mlp_model_2.p')
model_84 = pickle.load(open(model_path_2, 'rb'))['model']
labels_dict_42 = {0: 'C', 1: 'I', 2: 'L', 3: 'O', 4: 'U', 5: 'V'}
labels_dict_84 = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N', 11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z'}

# Load the math model
# Load the math model
model_path_num = os.path.join(os.path.dirname(__file__), 'mlp_model_num.p')
math_model = pickle.load(open(model_path_num, 'rb'))['model']
math_labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '0'}

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
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'letter': ''})

    category = data.get('category', 'general')  # Default to 'general' if not provided
    print(f"Received category: {category}")

    # Decode base64 image
    image_data = data['image'].split(',')[1]
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)
    H, W, _ = frame.shape

    # Process frame with Tasks API
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    results = landmarker.detect(mp_image)

    predicted_character = ''

    if results.hand_landmarks:
        data_aux = []
        # Support for multiple hands (matches old logic's data_aux accumulation)
        for hand_landmarks in results.hand_landmarks:
            x_ = [lm.x for lm in hand_landmarks]
            y_ = [lm.y for lm in hand_landmarks]
            
            # Normalize landmarks relative to each hand's bounding box min
            min_x = min(x_)
            min_y = min(y_)
            for i in range(len(hand_landmarks)):
                data_aux.append(x_[i] - min_x)
                data_aux.append(y_[i] - min_y)

        # Now data_aux will be 42 (one hand) or 84 (two hands)
        if category == "math":
            if len(data_aux) == 42:
                pred = math_model.predict([np.asarray(data_aux)])
                predicted_character = math_labels_dict.get(pred[0], '')
        else:
            if len(data_aux) == 42:
                pred = model_42.predict([np.asarray(data_aux)])
                predicted_character = labels_dict_42.get(pred[0], '')
            elif len(data_aux) == 84:
                pred = model_84.predict([np.asarray(data_aux)])
                predicted_character = labels_dict_84.get(pred[0], '')

    return jsonify({'letter': predicted_character})

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
    app.run(debug=True)
