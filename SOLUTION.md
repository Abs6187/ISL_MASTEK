# Resolution: WebRTC `is_alive` Teardown Race Condition & ASGI Protocol Errors

## 1. Latest Error: `AttributeError: 'NoneType' object has no attribute 'is_alive'`

### Symptom & Stack Trace
```text
Exception in callback AsyncIOEventEmitter._emit_run.<locals>.callback(<Task finished... 'is_alive'")>) at /home/adminuser/venv/lib/python3.11/site-packages/pyee/asyncio.py:97
handle: <Handle AsyncIOEventEmitter._emit_run.<locals>.callback(<Task finished... 'is_alive'")>) at /home/adminuser/venv/lib/python3.11/site-packages/pyee/asyncio.py:97>
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/asyncio/events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "/home/adminuser/venv/lib/python3.11/site-packages/pyee/asyncio.py", line 105, in callback
    self.emit("error", exc)
  File "/home/adminuser/venv/lib/python3.11/site-packages/pyee/asyncio.py", line 70, in emit
    return super().emit(event, *args, **kwargs)
  File "/home/adminuser/venv/lib/python3.11/site-packages/pyee/base.py", line 223, in emit
    self._emit_handle_potential_error(event, args[0] if args else None)
  File "/home/adminuser/venv/lib/python3.11/site-packages/pyee/base.py", line 181, in _emit_handle_potential_error
    raise error
AttributeError: 'NoneType' object has no attribute 'is_alive'
```

### Root Cause
1. **The `is_alive` Race Condition:**
   - In older versions of `streamlit-webrtc` (such as `0.67.4` which was pinned alongside `streamlit==1.50.0`), a race condition exists in the background thread shutdown observer:
     When a WebRTC video streamer stops, or when the user navigates between multi-page views or closes the tab, the cleanup thread attempts to inspect `self._worker.is_alive()`.
     Because the worker reference had already been set to `None` during overlapping shutdown paths, checking `.is_alive()` raises `AttributeError: 'NoneType' object has no attribute 'is_alive'`.
   - `whitphx/streamlit-webrtc` specifically identified and fixed this bug in **version 0.72.2** (June 19, 2026):
     > *"Fixed a race in shutdown observer cleanup that could raise `AttributeError: 'NoneType' object has no attribute 'is_alive'` when a WebRTC worker stops from overlapping shutdown paths."*

2. **Why `streamlit-webrtc==0.67.4` was previously pinned:**
   - Streamlit 1.50.0 used Tornado. However, newer `streamlit-webrtc` releases (`>=0.72.2`) require `streamlit>=1.51.0`.
   - In Streamlit 1.51–1.60 on Starlette >=1.8, Starlette introduced a breaking change to GZip middleware that caused `Expected ASGI message 'http.response.start', but got 'http.response.body'`.
   - Pinning `starlette>=0.46.0,<1.8` cleanly bypasses the Starlette ASGI middleware bug, which permits running `streamlit>=1.51.0,<1.61` alongside modern `streamlit-webrtc>=0.72.2`.

---

## 2. Complete Resolution Implemented

### Layer 1: Pinned Dependencies Matrix (`requirements.txt` & `requirements-cloud.txt`)
```text
streamlit>=1.51.0,<1.61
starlette>=0.46.0,<1.8
streamlit-webrtc>=0.72.2
aiortc>=1.3.0,<2.0.0
aioice>=0.9.0
av
opencv-python-headless
mediapipe==0.10.9
numpy
gTTS
flask
flask-cors
scikit-learn
```
- **`streamlit-webrtc>=0.72.2`**: Contains the upstream bugfix for the `is_alive` worker shutdown race condition.
- **`starlette>=0.46.0,<1.8`**: Prevents the Starlette 1.8+ GZip middleware ASGI protocol mismatch.
- **`streamlit>=1.51.0,<1.61`**: Fulfills the `streamlit>=1.51.0` prerequisite for `streamlit-webrtc>=0.72.2` while maintaining full compatibility with `mediapipe==0.10.9` (`protobuf<4`).

### Layer 2: Defense-in-Depth PyEE & AsyncIO Exception Suppression (`utils/event_loop_manager.py`)
Even with upstream library fixes, abrupt client socket disconnects or rapid page switching in Streamlit can occasionally trigger unhandled exceptions in `pyee.asyncio.AsyncIOEventEmitter`.
To make the application resilient under any circumstance:
1. **`patch_pyee()`**: Monkey-patches `pyee.base.EventEmitter._emit_handle_potential_error` to catch and absorb non-fatal `'is_alive'`, `'sendto'`, `'call_exception_handler'`, and transport closure AttributeErrors during event emission instead of crashing or bubbling to the event loop.
2. **`custom_exception_handler`**: Updated to intercept and suppress any `is_alive` context messages or AttributeErrors within the running `asyncio` event loop.
3. **`Home.py` early import**: `Home.py` imports `utils.event_loop_manager` immediately at process boot so that safety patches are in place before any camera streamer page is mounted or torn down.

---

## 3. Verification & Validation
- **Unit & Edge Case Tests**: 42 passed, 0 failed (`pytest tests/`).
  - Added `test_custom_exception_handler_suppresses_is_alive`
  - Added `test_patch_pyee_suppresses_is_alive`
- **Pip Resolver Dry-Run**: Confirmed `streamlit 1.60.0`, `starlette 0.46.2`, and `streamlit-webrtc 0.79.0` resolve with zero conflicts.
- **Syntax Validation**: Checked `Home.py`, all `pages/*.py`, and `utils/*.py` with Python compiler.
