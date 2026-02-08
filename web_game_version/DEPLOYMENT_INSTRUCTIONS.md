# Web Game Version - Deployment Instructions

This guide covers deploying the **Signify** ISL web game (Flask backend + static frontend).

---

## Prerequisites

- Python 3.11+
- Model files present: `mlp_model_1.p`, `mlp_model_2.p`, `mlp_model_num.p`, `models/hand_landmarker.task`
- (Optional) `PERPLEXITY_API_KEY` for the AI helper feature

---

## Option 1: Render (Recommended – Free Tier)

1. **Push to GitHub**  
   Ensure your repo is on GitHub.

2. **Create a Web Service**
   - Go to [render.com](https://render.com) → Sign in with GitHub
   - **New** → **Web Service**
   - Connect your repo
   - Configure:
     - **Root Directory:** `web_game_version`
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements-webgame.txt`
     - **Start Command:** `gunicorn server:app --bind 0.0.0.0:$PORT`
     - **Instance Type:** Free

3. **Environment Variables**
   - Add `PERPLEXITY_API_KEY` if you want the AI helper (optional).

4. **Create `requirements-webgame.txt`** (in `web_game_version/`):
   ```
   flask
   flask-cors
   gunicorn
   opencv-python-headless
   mediapipe>=0.10.0
   numpy
   scikit-learn
   requests
   python-dotenv
   ```

5. **Update `server.py`** for Render:
   - Change `app.run(debug=True)` to use `PORT`:
   ```python
   if __name__ == "__main__":
       port = int(os.environ.get("PORT", 5000))
       app.run(host="0.0.0.0", port=port)
   ```

6. **Deploy**  
   Click **Create Web Service**. Render will build and deploy.

---

## Option 2: Railway

1. **Push to GitHub.**

2. **Connect and Deploy**
   - Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
   - Select your repo
   - Set **Root Directory** to `web_game_version`

3. **Configure**
   - Add `requirements-webgame.txt` in `web_game_version/` (same as above)
   - Add `Procfile` in `web_game_version/`:
   ```
   web: gunicorn server:app --bind 0.0.0.0:$PORT
   ```

4. **Environment Variables**
   - Add `PERPLEXITY_API_KEY` (optional).

5. **Deploy**  
   Railway will auto-deploy from GitHub.

---

## Option 3: Docker (Self-host or Cloud)

1. **Create `web_game_version/Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-webgame.txt .
RUN pip install --no-cache-dir -r requirements-webgame.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD gunicorn server:app --bind 0.0.0.0:$PORT
```

2. **Build and Run:**
```bash
cd web_game_version
docker build -t isl-webgame .
docker run -p 8080:8080 -e PERPLEXITY_API_KEY=your_key isl-webgame
```

3. Deploy the image to AWS ECR, Google Cloud Run, Azure Container Apps, or any container host.

---

## Option 4: Heroku

1. **Install Heroku CLI**  
   [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Heroku app:**
```bash
cd web_game_version
heroku create your-isl-game
heroku config:set PERPLEXITY_API_KEY=your_key  # optional
```

3. **Add `Procfile`** in `web_game_version/`:
```
web: gunicorn server:app --bind 0.0.0.0:$PORT
```

4. **Add `runtime.txt`** in `web_game_version/`:
```
python-3.11.7
```

5. **Deploy:**
```bash
git subtree push --prefix web_game_version heroku main
# OR push the whole repo and set Heroku root to web_game_version in app settings
```

---

## Option 5: Local / VPS (Manual)

1. **Create virtual environment:**
```bash
cd web_game_version
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install flask flask-cors opencv-python-headless mediapipe numpy scikit-learn requests python-dotenv gunicorn
```

3. **Optional `.env` file:**
```
PERPLEXITY_API_KEY=your_key_here
```

4. **Run:**
```bash
# Development:
python server.py

# Production:
gunicorn server:app --bind 0.0.0.0:5000
```

5. Open `http://localhost:5000`

---

## Camera / WebRTC Note

Sign recognition needs the user’s webcam. The app captures video in the browser and sends frames to the `/predict` endpoint. This works in the cloud; no server-side camera is needed.

---

## Checklist Before Deploy

- [ ] All model files present (`mlp_model_1.p`, `mlp_model_2.p`, `mlp_model_num.p`, `models/hand_landmarker.task`)
- [ ] `requirements-webgame.txt` in `web_game_version/`
- [ ] `server.py` reads `PORT` env var (for Render/Railway/Heroku)
- [ ] `gunicorn` in requirements for production
- [ ] (Optional) `PERPLEXITY_API_KEY` set for AI helper

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Ensure all deps are in `requirements-webgame.txt` and installed |
| OpenCV errors on Linux | Use `opencv-python-headless` and install `libgl1-mesa-glx` |
| 502 / App not starting | Check logs; verify `gunicorn server:app` and `PORT` |
| AI helper fails | Add and set `PERPLEXITY_API_KEY` |
| Models not found | Confirm model paths and that they are in the deployed files |
