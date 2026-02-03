"""
WebRTC Utilities for Browser Camera Access
Provides shared configuration and helpers for streamlit-webrtc
"""

import logging

# Configure logging to suppress non-critical aioice errors
# These errors occur during connection cleanup and are non-fatal
logging.getLogger("aioice").setLevel(logging.ERROR)
logging.getLogger("aioice.ice").setLevel(logging.CRITICAL)
logging.getLogger("mediapipe").setLevel(logging.ERROR)

import streamlit as st
try:
    from twilio.rest import Client
except ImportError:
    Client = None
import os

def get_ice_servers():
    """
    Dynamically retrieve ICE servers from st.secrets or environment variables.
    prioirty:
    1. st.secrets["webrtc"]["iceServers"] (Direct list)
    2. st.secrets["webrtc"]["twilio"] (Twilio Dynamic Token)
    3. Default Google STUN servers
    """
    # 1. Check for direct iceServers in secrets
    if "webrtc" in st.secrets:
        if "iceServers" in st.secrets["webrtc"]:
            return st.secrets["webrtc"]["iceServers"]
        
        # 2. Check for Twilio credentials
        if "twilio" in st.secrets["webrtc"]:
            try:
                twilio_config = st.secrets["webrtc"]["twilio"]
                account_sid = twilio_config.get("account_sid")
                auth_token = twilio_config.get("auth_token")
                
                if account_sid and auth_token:
                    client = Client(account_sid, auth_token)
                    token = client.tokens.create()
                    return token.ice_servers
            except Exception as e:
                logging.warning(f"Failed to fetch Twilio ICE servers: {e}")
    
    # 3. Fallback to default free Google STUN servers
    return [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
    ]

# STUN/TURN server configuration for WebRTC
RTC_CONFIGURATION = {
    "iceServers": get_ice_servers(),
    # Try STUN/TURN relays and direct connections
    "iceTransportPolicy": "all",
    # Optimize ICE candidate gathering
    "iceCandidatePoolSize": 10,
}

# Media constraints
MEDIA_STREAM_CONSTRAINTS = {
    "video": True,
    "audio": False  # We don't need microphone for sign recognition
}

# Timeout configurations to prevent long-running operations
# These help prevent event loop issues during connection lifecycle
WEBRTC_CLIENT_SETTINGS = {
    # Maximum time to wait for media stream
    "media_stream_constraints": MEDIA_STREAM_CONSTRAINTS,
    # Async processing helps prevent blocking the main thread
    "async_processing": True,
}
