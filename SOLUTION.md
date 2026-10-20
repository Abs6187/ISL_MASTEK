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

## Fix applied

Pin Starlette below the breaking release and keep Streamlit in the range that works with mediapipe 0.10.9.
The same change is in both `requirements.txt` and `requirements-cloud.txt`:

```text
streamlit>=1.51.0,<1.61
starlette>=0.46.0,<1.8
```

Why this pair:

- `streamlit<1.61` stays within the versions that can coexist with `protobuf<4`. Streamlit 1.51 to 1.60
  all accept `protobuf>=3.20`.
- `starlette<1.8` avoids the changed gzip internals.
- `streamlit>=1.51.0` keeps it compatible with `streamlit-webrtc` 0.79.0, which requires
  `streamlit>=1.51.0`.

Earlier in this session both files pinned `streamlit==1.50.0`. That avoids the bug, but every recent
`streamlit-webrtc` (including 0.79.0 from your log) requires `streamlit>=1.51`. pip would have silently
downgraded `streamlit-webrtc` to an old release, so I replaced that pin.

## What you need to do

1. Commit and push `requirements.txt` and `requirements-cloud.txt`.
2. In Streamlit Community Cloud, open **Manage app → Reboot app** (the log shows dependencies are installed
   from `requirements.txt`).
3. Check the new log for the `Installed ... starlette==1.7.x` (or older) line and no more
   `Exception in ASGI application`.

## Not verified

- I did not run the full app against the new pin, and I did not redeploy. The pin is backed by the
  middleware reproduction and the dependency metadata, not by a finished end-to-end run.
- I did not check that Streamlit 1.51 to 1.59 are free of other bugs. The log only shows 1.60.0.
  Because the range is `>=1.51.0,<1.61`, pip will normally pick 1.60.0, the version in your log.

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
