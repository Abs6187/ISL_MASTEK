"""
WebRTC Utilities for Browser Camera Access
Provides shared configuration and helpers for streamlit-webrtc
"""

# STUN server configuration for WebRTC
# These help establish peer connections through firewalls
RTC_CONFIGURATION = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
    ]
}

# Media constraints
MEDIA_STREAM_CONSTRAINTS = {
    "video": True,
    "audio": False  # We don't need microphone for sign recognition
}
