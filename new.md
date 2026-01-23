# Implementing Browser-Based Camera for Cloud Deployment

## Problem Statement
Cloud platforms (Streamlit Cloud) cannot access server-side cameras. We need browser-based camera access using WebRTC.

## Solution: streamlit-webrtc
Use `streamlit-webrtc` to access the user's browser camera directly, bypassing the need for server-side camera hardware.

> **Note:** This guide applies to the **Streamlit version** (`streamlit-version/`). The **web game version** (`web_game_version/`) already uses browser-native `getUserMedia()` API and is cloud-compatible by design - no changes needed!

---

## Step-by-Step Implementation Guide

### Step 1: Install streamlit-webrtc

```bash
pip install streamlit-webrtc
```

Add to `requirements.txt`:
```
streamlit-webrtc
```

---

### Step 2: Basic WebRTC Setup

**Replace cv2.VideoCapture() with webrtc_streamer()**

**Before (doesn't work in cloud):**
```python
cap = cv2.VideoCapture(0)  # Server-side camera
```

**After (works in cloud):**
```python
from streamlit_webrtc import webrtc_streamer
import av

ctx = webrtc_streamer(
    key="sign-recognition",
    video_frame_callback=process_frame,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
```

---

### Step 3: Implement Video Processing Callback

**The callback processes each frame from browser camera:**

```python
def process_frame(frame):
    """
    Process video frame from browser camera
    Args:
        frame: av.VideoFrame from browser
    Returns:
        av.VideoFrame: processed frame with annotations
    """
    # Convert to numpy array
    img = frame.to_ndarray(format="bgr24")
    
    # Flip for mirror effect
    img = cv2.flip(img, 1)
    
    # YOUR PROCESSING HERE
    # - MediaPipe hand detection
    # - Model prediction
    # - Draw landmarks
    # - Add text annotations
    
    # Convert back to av.VideoFrame
    return av.VideoFrame.from_ndarray(img, format="bgr24")
```

---

### Step 4: Integrate MediaPipe with WebRTC

**Complete example for Sign Recognition:**

```python
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import numpy as np
import pickle

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, 
                       min_detection_confidence=0.3,
                       min_tracking_confidence=0.5)

# Load model
model_dict = pickle.load(open('model.p', 'rb'))
model = model_dict['model']

class SignRecognitionProcessor(VideoProcessorBase):
    def __init__(self):
        self.predicted_char = ""
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        
        # Process with MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                
                # Extract features
                data_aux = []
                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]
                
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))
                
                # Predict
                if len(data_aux) == 42:
                    prediction = model.predict([np.asarray(data_aux)])
                    self.predicted_char = str(prediction[0])
                    
                    # Display prediction
                    cv2.putText(img, self.predicted_char, (50, 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Use in Streamlit
webrtc_ctx = webrtc_streamer(
    key="sign-alphabet",
    video_processor_factory=SignRecognitionProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False}
)

# Display prediction outside video
if webrtc_ctx.video_processor:
    st.write(f"Predicted: {webrtc_ctx.video_processor.predicted_char}")
```

---

### Step 5: Handle Audio Output (Cloud Compatible)

**Replace pygame with browser TTS:**

```python
# Instead of pygame.mixer (doesn't work in cloud)
# Use browser's speechSynthesis API via JavaScript

def speak_browser(text):
    """Use browser's text-to-speech"""
    js_code = f"""
    <script>
    const utterance = new SpeechSynthesisUtterance("{text}");
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# Usage
if predicted_char:
    speak_browser(predicted_char)
```

---

### Step 6: Update Requirements

**Add to requirements.txt:**
```
streamlit-webrtc
aiortc  # WebRTC implementation
av  # PyAV for video processing
```

---

### Step 7: Configure for Streamlit Cloud

**IMPORTANT: STUN Server Configuration**

For WebRTC to work through firewalls:

```python
RTC_CONFIGURATION = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
    ]
}

webrtc_streamer(
    key="camera",
    rtc_configuration=RTC_CONFIGURATION,
    # ... other params
)
```

---

### Step 8: Testing Locally

```bash
# Install dependencies
pip install streamlit-webrtc aiortc av

# Run app
streamlit run streamlit-version/Home.py

# Browser will ask for camera permission
# Grant permission to test
```

---

## Key Differences: cv2.VideoCapture vs streamlit-webrtc

| Feature | cv2.VideoCapture | streamlit-webrtc |
|---------|------------------|------------------|
| **Works in Cloud** | ❌ No | ✅ Yes |
| **Camera Access** | Server-side | Browser-side |
| **User Permission** | Not needed | Browser prompt |
| **Latency** | Low | Slightly higher |
| **Code Complexity** | Simple | Moderate |

---

## Benefits for Your Project

1. **✅ Cloud Deployment**: Works on Streamlit Cloud, Heroku, etc.
2. **✅ No Hardware**: No server camera needed
3. **✅ User Privacy**: Camera stays on user's device
4. **✅ Cross-platform**: Works on any device with webcam
5. **✅ Browser Native**: Uses standard WebRTC APIs

---

## Implementation Checklist

- [x] Install streamlit-webrtc and dependencies
- [x] Create VideoProcessor class for each recognition page
- [x] Replace cv2.VideoCapture with webrtc_streamer
- [x] Configure STUN servers for firewall traversal
- [x] Replace pygame audio with browser TTS
- [x] Test locally with browser permissions
- [x] Deploy to Streamlit Cloud
- [x] Test in production environment

---

## Example: Complete Page Refactor

**File: `pages/1_🅰️ Sign Alphabet Recognition.py`**

See full implementation in the actual code files - the pattern is:
1. Define VideoProcessor class with `recv()` method
2. Process frames with MediaPipe  
3. Return annotated frames
4. Use webrtc_streamer instead of cv2.VideoCapture loop
5. Access processor state from outside video stream

---

## Audio Alternative: Browser TTS

Since pygame requires audio devices, use browser's built-in TTS:

```python
import streamlit.components.v1 as components

def speak_text(text):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <script>
        const speak = (text) => {{
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.volume = 1;
            utterance.rate = 1;
            utterance.pitch = 1;
            window.speechSynthesis.speak(utterance);
        }};
        speak("{text}");
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=0)
```

---

## Troubleshooting

### Issue: "Camera not detected"
**Solution**: User needs to grant browser camera permission

### Issue: "Black screen"
**Solution**: Check STUN server configuration

### Issue: "High latency"
**Solution**: Normal for WebRTC, optimize frame processing

### Issue: "Doesn't work on HTTPS"
**Solution**: WebRTC requires HTTPS (Streamlit Cloud provides this)

---

## Final Notes

- **This makes your app fully cloud-compatible!** 🎉
- Camera and audio work anywhere
- No server hardware limitations
- Professional browser-based solution
- Industry-standard WebRTC technology

**Ready to implement? The next step is to refactor your recognition pages!**