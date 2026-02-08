# Flask Web Game (ISL) - for Render / Docker
FROM python:3.11-slim

WORKDIR /app

# System deps for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-webgame.txt .
RUN pip install --no-cache-dir -r requirements-webgame.txt

COPY . .

# Render sets PORT; default for local
ENV PORT=5000
EXPOSE 5000

# Gunicorn for production (PORT set by Render at runtime)
CMD ["sh", "-c", "gunicorn server:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 2"]
