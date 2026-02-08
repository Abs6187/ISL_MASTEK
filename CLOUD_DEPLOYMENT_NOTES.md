# Cloud Deployment Notes

## 🌐 WebRTC Network Configuration

### 1. Default Configuration (Google STUN)
By default, the application is configured to use **Google's public STUN servers** (`stun.l.google.com:19302`). 
**No additional configuration or secrets are required** for this to work in most open network environments.

### 2. Troubleshooting Connection Issues
If you encounter the error **"Check your network connection"** or the video spinner runs forever, it likely means the default STUN server is blocked by a firewall or symmetric NAT (common in corporate/university networks).

In this case, you must provide a **TURN server**.

#### Option: Add TURN Server via Secrets (Optional)
You can configure a custom STUN/TURN server without changing the code by adding it to your Streamlit Secrets.

**Using Twilio (Recommended for reliability):**
1.  Get Account SID and Auth Token from Twilio Console.
2.  Add to `.streamlit/secrets.toml` (local) or Streamlit Cloud Secrets:

```toml
[webrtc.twilio]
account_sid = "your_account_sid_here"
auth_token = "your_auth_token_here"
```

**Using Custom/Free TURN (e.g. Metered.ca):**
```toml
[webrtc]
iceServers = [
    { urls = ["stun:stun.l.google.com:19302"] },
    { urls = ["turn:your.turn.server:80"], username = "user", credential = "password" }
]
```

---

## 🎤 PyAudio and Microphone Access

### Issue:
PyAudio fails to build in cloud environments because it requires:
- System-level PortAudio libraries
- Direct hardware (microphone) access
- Which cloud platforms don't provide

### Solution Options:

#### Option 1: Skip PyAudio (Recommended for Cloud)
Use `requirements-cloud.txt` instead of `requirements.txt`:

```bash
# For Streamlit Cloud deployment
# In settings, specify: requirements-cloud.txt
```

This file excludes PyAudio and SpeechRecognition since they won't work in cloud anyway.

#### Option 2: Keep Full Requirements (CI/CD)
The GitHub Actions workflow now installs system dependencies:
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
```

This allows tests to pass, but features still won't work in cloud deployment.

### Affected Features:
- ✅ **Work in Cloud:**
  - Sign Alphabet Recognition
  - Sign Number Recognition
  - Text-to-Sign Translation
  - Web Game Version

- ❌ **Don't Work in Cloud:**
  - Speech-to-Sign Translation (requires microphone)
  - Audio output features (can be replaced with browser TTS)

### Recommendations:

1. **For Cloud Deployment (Streamlit Cloud, Heroku):**
   - Use `requirements-cloud.txt`
   - Disable speech input features
   - Use text input instead
   - Document limitations in README

2. **For Local Development:**
   - Use full `requirements.txt`
   - Install PortAudio:
     - **Windows:** Already bundled with PyAudio wheel
     - **Mac:** `brew install portaudio`
     - **Linux:** `sudo apt-get install portaudio19-dev`

3. **For Docker:**
   - Dockerfile now includes portaudio19-dev
   - But still limited by no microphone access

### Alternative: Browser-Based Audio
Consider using:
- Web Audio API for browser-based microphone access
- Streamlit components for audio recording
- External speech-to-text services

### Updated Deployment Instructions:

**Streamlit Cloud:**
1. In app settings, specify: `requirements-cloud.txt`
2. Or modify `requirements.txt` to comment out PyAudio
3. Document in UI that speech features require local deployment

**Heroku:**
```bash
# Add buildpack for PortAudio (optional but complex)
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Or use requirements-cloud.txt
```

**Docker:**
- Already configured with PortAudio
- But won't have microphone access in container

---

## Deploy Flask App (Web Game) on Render

Use these steps to deploy the **Flask** web game (ISL) as a separate Web Service on Render with **Docker**. (Streamlit is a separate deployment; this is only for the Flask app in `web_game_version/`.)

### 1. Repository and service type

- **Source:** Connect your repo (e.g. GitHub) and select the repo (e.g. `Abs6187/ISL_MASTEK`).
- **Create:** **Web Service** (not Background Worker).
- **Name:** e.g. `ISL_MASTEK` or `isl-flask`.

### 2. Build & runtime

- **Language:** **Docker**.
- **Branch:** `main` (or your default branch).
- **Region:** e.g. Singapore (Southeast Asia) or your preferred region.

### 3. Root directory (required)

So Render builds and runs only the Flask app:

- **Root Directory:** `web_game_version`

Render will run all commands and use the Dockerfile from this directory. Only changes under `web_game_version/` will trigger auto-deploys if you use path filters.

### 4. Docker settings

- **Docker Build Context Directory:** `.` (relative to Root Directory, so the context is `web_game_version/`).
- **Dockerfile Path:** `./Dockerfile` (the one inside `web_game_version/`).
- **Docker Command:** Leave empty so the Dockerfile `CMD` is used (Gunicorn).

### 5. Instance type

- **Free:** 512 MB RAM — okay for light use; instance spins down when idle.
- **Starter ($7/mo)** or higher if you need always-on and better performance.

### 6. Environment variables

Add in the Render dashboard under **Environment**:

| Name | Value | Notes |
|------|--------|--------|
| `PORT` | *(leave empty)* | Render sets this automatically. |
| `FLASK_DEBUG` | `false` | Optional; set `true` only for temporary debugging. |
| `PERPLEXITY_API_KEY` | *your key* | Optional; only if you use the “Ask AI” feature in the web game. |

No need to set `PORT` manually; Render injects it.

### 7. Health check

- **Health Check Path:** `/healthz`

The Flask app exposes `/healthz` for Render’s health checks. If you leave this blank, Render may still use the root URL.

### 8. Advanced (optional)

- **Pre-Deploy Command:** Leave empty unless you add migrations or asset steps later.
- **Auto-Deploy:** **On** (deploy on push to the selected branch).
- **Build Filters – Included Paths:** Add `web_game_version` so only changes in the Flask app trigger deploys (optional).

### 9. Deploy

Click **Create Web Service**. Render will:

1. Clone the repo and `cd` into `web_game_version` (Root Directory).
2. Build the image using `web_game_version/Dockerfile`.
3. Run the container; the startup command is Gunicorn bound to `0.0.0.0:${PORT}`.
4. Hit `/healthz` for health checks.

After the first successful deploy, your Flask app URL will be like:

`https://<your-service-name>.onrender.com`

### 10. Files used by this deployment

- `web_game_version/Dockerfile` — Docker build for the Flask app only.
- `web_game_version/server.py` — Flask app; includes `/healthz` and serves the frontend.
- `web_game_version/requirements-webgame.txt` — Python dependencies for the web game.
- Models and frontend under `web_game_version/` are copied into the image by the Dockerfile.

### Troubleshooting

- **Build fails:** Ensure **Root Directory** is exactly `web_game_version` and the Dockerfile path is `./Dockerfile`.
- **Service not starting:** Check **Logs** in Render; ensure no Python import errors (e.g. missing files under `web_game_version/`).
- **502 / unhealthy:** Confirm **Health Check Path** is `/healthz` and that the app listens on `0.0.0.0` and the port Render provides (handled by the Dockerfile `CMD`).
