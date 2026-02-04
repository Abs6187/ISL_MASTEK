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
    # Try to access secrets - handle case when secrets.toml doesn't exist
    try:
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
                        if Client is None:
                            logging.warning("Twilio client not available - twilio package not installed")
                        else:
                            client = Client(account_sid, auth_token)
                            token = client.tokens.create()
                            return token.ice_servers
                except Exception as e:
                    logging.warning(f"Failed to fetch Twilio ICE servers: {e}")
    except Exception as e:
        # secrets.toml doesn't exist or can't be read - this is fine, use defaults
        logging.debug(f"No secrets available, using default STUN servers: {e}")
    
    # 3. Fallback to multiple free STUN servers for better connectivity
    # Using servers from different providers improves NAT traversal
    return [
        # Google STUN servers
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        # Cloudflare STUN
        {"urls": ["stun:stun.cloudflare.com:3478"]},
        # Twilio STUN (free)
        {"urls": ["stun:global.stun.twilio.com:3478"]},
        # Microsoft STUN
        {"urls": ["stun:stunserver.stunprotocol.org:3478"]},
    ]

# STUN/TURN server configuration for WebRTC
RTC_CONFIGURATION = {
    "iceServers": get_ice_servers(),
    # Try STUN/TURN relays and direct connections
    "iceTransportPolicy": "all",
    # Optimize ICE candidate gathering
    "iceCandidatePoolSize": 0,  # Use browser default (10 can cause issues)
}

# Media constraints with explicit video settings for better compatibility
MEDIA_STREAM_CONSTRAINTS = {
    "video": {
        "facingMode": "user",  # Prefer front camera
        "width": {"ideal": 640, "max": 1280},
        "height": {"ideal": 480, "max": 720},
        "frameRate": {"ideal": 15, "max": 30},
    },
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
