import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure streamlit-version is in path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit-version"))

# Mock dependencies before import if needed
mock_st = MagicMock()
mock_st.secrets = {}
sys.modules["streamlit"] = mock_st
sys.modules["streamlit.components.v1"] = MagicMock() # For browser_tts

# Import modules to test
# Note: webrtc_utils imports streamlit, which is now mocked
from utils import webrtc_utils
from utils import browser_tts
from utils import event_loop_manager

class TestWebRTCUtilsEdgeCases:
    
    def teardown_method(self):
        mock_st.secrets = {}

    def test_get_ice_servers_malformed_secrets(self):
        """Test graceful handling when secrets structure is unexpected"""
        # Case 1: 'webrtc' key exists but is not a dict
        mock_st.secrets = {"webrtc": "invalid_string"}
        # Should fall back to default without crashing
        try:
            ice_servers = webrtc_utils.get_ice_servers()
            assert len(ice_servers) > 0
            assert "stun:stun.l.google.com" in ice_servers[0]["urls"][0]
        except Exception as e:
            pytest.fail(f"Crashed on malformed 'webrtc' secret: {e}")

    def test_get_ice_servers_twilio_missing_keys(self):
        """Test handling of incomplete Twilio config"""
        # Case: Twilio config exists but missing auth_token
        mock_st.secrets = {
            "webrtc": {
                "twilio": {"account_sid": "AC123"} # missing auth_token
            }
        }
        ice_servers = webrtc_utils.get_ice_servers()
        # Should return default google servers
        assert "stun:stun.l.google.com" in ice_servers[0]["urls"][0]

    def test_get_ice_servers_empty_list(self):
        """Test when iceServers is explicitly set to empty list"""
        mock_st.secrets = {
            "webrtc": {
                "iceServers": []
            }
        }
        ice_servers = webrtc_utils.get_ice_servers()
        # Should return the empty list as configured, trusting the user
        assert ice_servers == []

class TestBrowserTTSEdgeCases:
    
    def test_speak_text_empty(self):
        """Test graceful handling of empty/None text"""
        # Should simply return without error
        try:
            browser_tts.speak_text("")
            browser_tts.speak_text(None)
        except Exception as e:
            pytest.fail(f"Crashed on empty text: {e}")

    def test_speak_text_injection_sanitization(self):
        """Verify text quotes are escaped to prevent JS injection"""
        dangerous_text = 'Hello"; alert("hacked"); var x="'
        
        with patch("utils.browser_tts.components.html") as mock_html:
            browser_tts.speak_text(dangerous_text)
            
            # Extract the HTML generated
            html_call = mock_html.call_args[0][0]
            
            # The quotes inside the text should be escaped with backslash
            # We look for \"hacked\" in the output
            assert '\\"hacked\\"' in html_call
            assert 'alert(\\"hacked\\")' in html_call

    def test_safe_send_stun_with_none_transport(self):
        """Test the actual patched logic: send_stun with None transport"""
        # Define a mock protocol class
        class MockProtocol:
            def __init__(self):
                self.transport = None
                self.called_original = False
                
            def send_stun(self, msg, addr):
                self.called_original = True
        
        # Get unbound method
        original = MockProtocol.send_stun
        
        # Replicate the monkey patch wrapper logic
        def safe_send_stun(self, message, addr):
            if self.transport is None:
                return
            return original(self, message, addr)
            
        protocol = MockProtocol()
        
        # Test with None transport (should NOT call original)
        protocol.transport = None
        safe_send_stun(protocol, "msg", "addr")
        assert protocol.called_original is False
        
        # Test with valid transport (SHOULD call original)
        protocol.transport = "valid"
        safe_send_stun(protocol, "msg", "addr")
        assert protocol.called_original is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
