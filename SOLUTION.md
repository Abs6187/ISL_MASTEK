# Fix: `Expected ASGI message 'http.response.start'` on Streamlit Cloud

Source: deployment log `logs-abs6187-isl_mastek-main-streamlit-version-Home.py-2026-10-20T05_59_47.048Z.txt`
(app `isl-mastek.streamlit.app`, main module `streamlit-version/Home.py`).

## Symptom

The log has about 50 repeated tracebacks, starting right after `Uvicorn server started on :::8501`:

```
Exception in ASGI application
  ...
  File ".../streamlit/web/server/starlette/starlette_gzip_middleware.py", line 105, in send_with_compression
    await super().send_with_compression(message)
  File ".../starlette/middleware/gzip.py", line 125, in send_with_compression
  ...
RuntimeError: Expected ASGI message 'http.response.start', but got 'http.response.body'.
```

The app's own Python code never appears in these tracebacks. They come from Streamlit's web server
while it serves its own static files and routes.

## Root cause

The deploy resolved this combination (taken from the log):

| Package | Version |
|---|---|
| `streamlit` | 1.60.0 |
| `starlette` | **1.9.0** |
| `uvicorn` | 0.54.0 |
| `protobuf` | 3.20.3 |
| `mediapipe` | 0.10.9 |

Two things combine:

1. **Streamlit 1.60.0 subclasses Starlette's gzip internals.** Its `starlette_gzip_middleware.py`
   overrides `send_with_compression` on Starlette's `IdentityResponder` and `GZipResponder`. For an
   `http.response.start` message it only records the headers and never forwards the message.
2. **Starlette 1.8.0 changed those internals.** Starlette's own `send_with_compression` now forwards
   `http.response.start` immediately for responses that are already encoded, partial (206), or have an
   excluded content type (images, fonts, audio and so on). Streamlit's override skips that code, so the
   next `http.response.body` reaches uvicorn with no start message, and uvicorn raises the error.

**Why Streamlit isn't simply upgraded:** `mediapipe==0.10.9` requires `protobuf<4`. Streamlit 1.61 and
newer require `protobuf>=5.26.1`, so pip/uv cannot install them next to mediapipe 0.10.9. That is why the
resolver stayed on 1.60.0. A newer mediapipe is not a drop-in fix either: `mediapipe>=0.10.33` no longer
has `mp.solutions`, which `pages/1_Sign_Alphabet_Recognition.py` and `pages/2_Sign_Number_Recognition.py`
use (`mp.solutions.hands`).

## Evidence

Checked by running Streamlit's real `SelectiveGZipMiddleware` against a mock app that sends a
`image/png` response, with a send function that rejects a body before a start message (as uvicorn does):

| Streamlit | Starlette | Result |
|---|---|---|
| 1.60.0 | 1.4.1, 1.5.0, 1.6.0, **1.7.0** | OK |
| 1.60.0 | **1.8.0**, 1.9.0 | **FAILED** (same error as the log) |
| 1.61.0 | 1.9.0 | FAILED |
| 1.62.0, 1.63.0, 1.66.0 | 1.9.0 | OK |

- Starlette 1.7.0 is the last good version and 1.8.0 is the first bad one.
- Streamlit 1.62.0 is the first release that works with Starlette 1.9.0, but it needs `protobuf>=5.26.1`
  and so conflicts with mediapipe 0.10.9.
- A live Streamlit 1.60.0 + Starlette 1.9.0 server returned **HTTP 500** for `/favicon.png`. I interrupted
  that run before it finished, so the full set of failing URLs was not captured.
- I confirmed with `uv pip compile` that `streamlit>=1.62` + `mediapipe==0.10.9` is unsatisfiable.

## Fix applied (proven by the second deploy log)

The second log (`...06_52_12...txt`) covers a redeploy at 06:32 UTC of commit `9808dc3`, which pinned
`streamlit==1.50.0`. That redeploy:

- swapped `streamlit` 1.60.0 -> **1.50.0** (Tornado server, no Starlette gzip middleware) and
  `streamlit-webrtc` 0.79.0 -> **0.67.4**;
- shows **no `Exception in ASGI application` after the swap** (the two 500s on `/favicon.png` at
  06:32:04 and 06:32:07 are the old process still serving while packages were replaced, right before
  `Shutting down` / `Updated app!`);
- shows a MediaPipe session running at 06:50 (`Created TensorFlow Lite XNNPACK delegate for CPU`).

So the final pins, in both `requirements.txt` and `requirements-cloud.txt`, are the configuration observed
working:

```text
streamlit==1.50.0
streamlit-webrtc==0.67.4
```

`streamlit-webrtc` is pinned to 0.67.4 because that is what pip resolved for Streamlit 1.50.0: every
recent `streamlit-webrtc` (including 0.79.0 from the first log) requires `streamlit>=1.51`. Leaving it as
`>=0.47.0` meant the resolver silently chose an old release. 0.67.4 needs `aiortc>=1.14.0` and
`aioice>=0.10.1`, which fit the existing `aiortc>=1.3.0,<2.0.0` and `aioice>=0.9.0` specs.

### Alternative that was tried and replaced

Commit `e4a2a4d` (`streamlit>=1.51.0,<1.61` + `starlette>=0.46.0,<1.8`) is based on the middleware tests
above and should also avoid the crash, but it has **no deploy log showing it working**, and it moves the
app back to Streamlit 1.60.x + `streamlit-webrtc` 0.79.0. Since 1.50.0 is proven in production, the files now
use that. If you want to move to 1.60.x later, that Starlette pin is the way to do it.

## What you need to do

1. Commit and push `requirements.txt`, `requirements-cloud.txt` and this file.
2. Reboot the app in Streamlit Community Cloud (**Manage app -> Reboot app**).
3. Check the new log for `streamlit==1.50.0` / `streamlit-webrtc==0.67.4` and no
   `Exception in ASGI application`.

## Not verified

- The 1.50.0 result comes from your log, not from my own run. I did not install anything locally.
- The log has no entries after 06:50, so it doesn't show every page (for example Speech-to-Sign or
  Camera Test) being opened after the swap.
- `streamlit-elements` was removed from `requirements.txt` in `9808dc3`. A search of the Python sources
  found no imports of it, so nothing should break, but I did not run every page.

## Other messages in the log (not errors)

- `H5 model not available: No module named 'tensorflow'`: the Alphabet/Number pages try to import
  TensorFlow for the optional `sign_language_recognition.h5` model inside a `try/except`. It is logged as
  a warning and the app falls back to the MLP model. Fixing it would mean adding `tensorflow` to the
  requirements, which is large and not needed. I left it alone.
- `"general.email" is not a valid config option`: this was in an older `.streamlit/config.toml`. The file
  on disk no longer has it, so it should be gone after the next deploy.

## Longer-term options

- Move off `mp.solutions` to the MediaPipe Tasks API (`HandLandmarker`; `hand_landmarker.task` is already
  in `assets/models/`), then remove the `mediapipe==0.10.9` pin. That lifts the `protobuf<4` cap and lets
  you use Streamlit 1.62 or newer, where this bug is fixed, without the Starlette pin.
