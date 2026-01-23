# Cloud Deployment Notes

## PyAudio and Microphone Access

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
