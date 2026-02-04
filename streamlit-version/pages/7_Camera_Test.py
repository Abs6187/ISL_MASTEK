import streamlit as st
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.webrtc_utils import RTC_CONFIGURATION, MEDIA_STREAM_CONSTRAINTS
# Import event loop manager to suppress aioice warnings
import utils.event_loop_manager
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import numpy as np

st.set_page_config(page_title="Camera Test", page_icon="🎥", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0E1117 0%, #1a1d29 50%, #262730 100%);
        }
        h1, h2 {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 50%, #00BCD4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    </style>
    <h1 style="text-align: center;">🎥 Camera Test Page</h1>
""", unsafe_allow_html=True)

st.markdown("""
    This page is for testing if your camera works with the application.
    If you see a video feed here, your camera is working correctly!
""")

# Display current configuration
with st.expander("🔧 WebRTC Configuration (for debugging)", expanded=False):
    st.json(RTC_CONFIGURATION)
    st.json(MEDIA_STREAM_CONSTRAINTS)

st.markdown("---")

st.info("📹 Click 'START' below and grant camera permission when prompted.")

class SimpleProcessor(VideoProcessorBase):
    """Simple video processor that just passes frames through"""
    
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # Add timestamp
        import time
        ts = time.strftime("%H:%M:%S")
        cv2.putText(img, f"Camera Test - {ts}", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="camera-test",
    video_processor_factory=SimpleProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints=MEDIA_STREAM_CONSTRAINTS,
    async_processing=True,
)

st.markdown("---")

# Status information
st.markdown("### Status")
col1, col2 = st.columns(2)

with col1:
    if webrtc_ctx.state.playing:
        st.success("🟢 Camera is **Active**")
    else:
        st.warning("⚪ Camera is **Inactive**")

with col2:
    if webrtc_ctx.video_processor:
        st.success("✅ Video processor is **Running**")
    else:
        st.warning("⚠️ Video processor is **Not Running**")

# Troubleshooting guide
st.markdown("---")
st.markdown("### Troubleshooting")

st.markdown("""
#### Camera shows black screen or won't start:
1. **Browser Permissions**: Make sure you've allowed camera access when prompted
2. **Browser Compatibility**: Use Chrome or Edge for best results
3. **HTTPS Required**: Camera only works on HTTPS or localhost (not HTTP)
4. **Firewall**: Ensure WebRTC traffic isn't being blocked
5. **Network**: Try a different network if you're behind a restrictive firewall

#### Camera light is on but no video:
1. Another app might be using the camera
2. Try refreshing the page
3. Try using a different browser

#### Still having issues?
Check the browser console for errors (F12 → Console tab)
""")

# Additional diagnostics
st.markdown("---")
st.markdown("### Browser Compatibility Check")

st.markdown("""
| Browser | Status |
|---------|--------|
| Chrome | ✅ Fully supported |
| Edge | ✅ Fully supported |
| Firefox | ⚠️ May have issues |
| Safari | ⚠️ May have issues |
| Mobile Browsers | ⚠️ May have issues |
""")

st.markdown(
    "### Current Configuration\n"
    f"- **ICE Servers**: {len(RTC_CONFIGURATION['iceServers'])} servers configured\n"
    "- **Video Resolution**: Ideal 640x480, Max 1280x720\n"
    "- **Frame Rate**: Ideal 15 FPS, Max 30 FPS\n"
    "- **Audio**: Disabled (not needed for sign recognition)"
)
