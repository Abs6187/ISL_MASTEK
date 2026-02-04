"""
Event Loop Lifecycle Management for WebRTC in Streamlit

This module provides utilities to handle asyncio event loop issues
that occur when using streamlit-webrtc with aiortc backend.

Known Issues:
- aioice retry errors during connection cleanup
- Event loop becoming None during STUN retries
- Timer callbacks executing after transport closure

Solution Approach:
- Suppress non-critical retry errors
- Provide graceful cleanup hooks
- Configure timeouts to minimize retry attempts
"""

import asyncio
import logging
import warnings
import sys
from contextlib import contextmanager

# Configure logging
from typing import Dict, Any

# Suppress aioice and mediapipe warnings
def suppress_aioice_warnings():
    """Suppress aioice and mediapipe logging warnings."""
    # Set aioice logger to CRITICAL to suppress all warnings and errors
    aioice_logger = logging.getLogger('aioice')
    aioice_logger.setLevel(logging.CRITICAL)
    
    # Set aiortc logger to ERROR
    aiortc_logger = logging.getLogger('aiortc')
    aiortc_logger.setLevel(logging.ERROR)
    
    # Set mediapipe logger to ERROR
    mediapipe_logger = logging.getLogger('mediapipe')
    mediapipe_logger.setLevel(logging.ERROR)
    
    # Also suppress absl logging (used by MediaPipe)
    try:
        import absl.logging
        absl.logging.set_verbosity(absl.logging.ERROR)
        absl.logging.set_stderrthreshold(absl.logging.ERROR)
    except ImportError:
        pass


def custom_exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]):
    """
    Custom asyncio exception handler to suppress known non-fatal errors.
    
    This handler specifically suppresses:
    - aioice 'NoneType' sendto errors
    - aioice 'NoneType' call_exception_handler errors
    - Other transport/event loop lifecycle errors
    """
    exception = context.get('exception')
    message = context.get('message', '')
    
    # Suppress aioice NoneType errors (non-fatal)
    if isinstance(exception, AttributeError):
        error_msg = str(exception)
        if "'NoneType' object has no attribute 'sendto'" in error_msg:
            # Silently ignore - this is expected during WebRTC teardown
            return
        if "'NoneType' object has no attribute 'call_exception_handler'" in error_msg:
            # Silently ignore - this is expected during event loop cleanup
            return
    
    # Suppress "Task was destroyed but it is pending!" for aioice
    if 'Task was destroyed but it is pending!' in message:
        if 'aioice' in message or 'Transaction.__retry' in message:
            return
    
    # For any other exceptions, use default handler
    # This ensures we don't hide genuinely important errors
    try:
        if loop is not None:
            loop.default_exception_handler(context)
    except Exception:
        # If the event loop is also None, we can't handle this - just suppress
        pass


def configure_event_loop_policy():
    """
    Configure the event loop policy for Windows compatibility.
    Sets up custom exception handler to suppress aioice errors.
    """
    if sys.platform == 'win32':
        # Use ProactorEventLoop on Windows for better subprocess support
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Get or create event loop and set custom exception handler
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Set custom exception handler to suppress aioice errors
    loop.set_exception_handler(custom_exception_handler)


class WebRTCConnectionManager:
    """
    Manager for tracking WebRTC connections and their lifecycle.
    
    This can be used to ensure proper cleanup of connections
    during Streamlit reruns.
    """
    
    def __init__(self):
        self.active_connections = set()
    
    def register_connection(self, connection_id: str):
        """Register a new WebRTC connection."""
        self.active_connections.add(connection_id)
    
    def unregister_connection(self, connection_id: str):
        """Unregister a WebRTC connection."""
        self.active_connections.discard(connection_id)
    
    def cleanup_all(self):
        """Cleanup all registered connections."""
        self.active_connections.clear()


# Global connection manager instance
connection_manager = WebRTCConnectionManager()

# Apply configurations on module import
suppress_aioice_warnings()
configure_event_loop_policy()




def patch_aioice():
    """
    Monkey-patch aioice to prevent AttributeError: 'NoneType' object has no attribute 'sendto'
    during event loop teardown.
    
    This patches both the high-level send_stun method and the low-level socket operations
    to handle closed transports gracefully.
    """
    try:
        import aioice.ice
    except ImportError:
        return

    # Patch 1: Safe send_stun method
    if not hasattr(aioice.ice.StunProtocol, '_original_send_stun'):
        aioice.ice.StunProtocol._original_send_stun = aioice.ice.StunProtocol.send_stun

    def safe_send_stun(self, message, addr):
        # Check if transport exists and is healthy before using it
        if self.transport is None:
            # Transport is closed, silently ignore
            return
        try:
            return self._original_send_stun(message, addr)
        except (AttributeError, OSError, ConnectionResetError):
            # Ignore any errors that occur during send on closing transport
            return

    # Apply patch to StunProtocol
    aioice.ice.StunProtocol.send_stun = safe_send_stun
    
    # Patch 2: Safe datagram_protocol_sendto for asyncio selector events
    try:
        from asyncio.selector_events import _SelectorDatagramTransport
    except ImportError:
        _SelectorDatagramTransport = None
    
    if _SelectorDatagramTransport is not None:
        if not hasattr(_SelectorDatagramTransport, '_original_sendto'):
            _SelectorDatagramTransport._original_sendto = _SelectorDatagramTransport.sendto
        
        def safe_sendto(self, data, addr=None):
            # Check if socket exists before sending
            if self._sock is None:
                # Socket is closed, silently ignore
                return
            if hasattr(self, '_closing') and self._closing:
                # Transport is closing, silently ignore
                return
            try:
                return self._original_sendto(data, addr)
            except (AttributeError, OSError, ConnectionResetError, ValueError):
                # Ignore errors from closed socket
                return
        
        # Apply patch
        _SelectorDatagramTransport.sendto = safe_sendto


# Initialize on module import
suppress_aioice_warnings()
patch_aioice()  # Apply safety patch
configure_event_loop_policy()

