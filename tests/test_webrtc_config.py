import sys
import os
import importlib
from unittest.mock import MagicMock, patch

# Add streamlit-version directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit-version"))

# Mock streamlit and twilio BEFORE importing utils
# This is necessary because webrtc_utils accesses st.secrets at module level
mock_st = MagicMock()
mock_st.secrets = {}
sys.modules["streamlit"] = mock_st
sys.modules["twilio.rest"] = MagicMock()

from utils import webrtc_utils

import pytest # Import pytest after mocking if needed, or keeping it top level is fine usually, but let's be safe.
# Actually pytest needs to be imported to run.

class TestWebRTCConfig:
    
    def setup_method(self):
        """Reload utils to ensure proper mocking before each test"""
        importlib.reload(webrtc_utils)

    def teardown_method(self):
        """Reset secrets after each test"""
        mock_st.secrets = {}

    def test_default_ice_servers(self):
        """Test that default Google STUN servers are returned when no secrets exist"""
        # Ensure secrets are empty
        mock_st.secrets = {}
        
        # Reload module to re-run top-level code if needed, 
        # BUT get_ice_servers is a function, so we can just call it.
        # However, RTC_CONFIGURATION is a constant set at import time.
        # We should test get_ice_servers() directly content.
        
        ice_servers = webrtc_utils.get_ice_servers()
        assert len(ice_servers) > 0
        # Check defaults
        found_google = any("stun.l.google.com" in s["urls"][0] for s in ice_servers)
        assert found_google

    def test_secrets_ice_servers(self):
        """Test that iceServers from secrets are used if present"""
        mock_secrets = {
            "webrtc": {
                "iceServers": [{"urls": ["stun:mock.stun.server"]}]
            }
        }
        mock_st.secrets = mock_secrets
        
        ice_servers = webrtc_utils.get_ice_servers()
        assert len(ice_servers) == 1
        assert ice_servers[0]["urls"] == ["stun:mock.stun.server"]

    def test_twilio_integration(self):
        """Test that Twilio client is called when Twilio credentials are provided"""
        mock_secrets = {
            "webrtc": {
                "twilio": {
                    "account_sid": "AC123",
                    "auth_token": "token123"
                }
            }
        }
        mock_st.secrets = mock_secrets
                
        # Get the mock client we set up in sys.modules
        MockClient = sys.modules["twilio.rest"].Client
        mock_instance = MockClient.return_value
        mock_token = mock_instance.tokens.create.return_value
        mock_token.ice_servers = [{"urls": "turn:mock.twilio.turn"}]
            
        ice_servers = webrtc_utils.get_ice_servers()
        
        # Check if Client was initialized with correct creds
        MockClient.assert_called_with("AC123", "token123")
        # Check if we got the ice_servers from the token
        assert ice_servers == [{"urls": "turn:mock.twilio.turn"}]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
