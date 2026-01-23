# Deployment Guide - Bidirectional ISL System

This guide provides instructions for deploying the ISL Communication System.

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Free, Easy, and Fast!**

#### Steps:

1. **Fork or Push to GitHub**
   - Your code is already on GitHub at: `https://github.com/Abs6187/ISL_MASTEK`

2. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy New App**
   - Click "New app"
   - Repository: `Abs6187/ISL_MASTEK`
   - Branch: `main`
   - Main file path: `streamlit-version/Home.py`
   - Click "Deploy!"

4. **Configuration**
   - The `.streamlit/config.toml` file will automatically apply your Material UI theme
   - App will be deployed at: `https://[your-app-name].streamlit.app`

#### ⚠️ Important Notes for Streamlit Cloud:
- Camera features may not work in cloud deployment (requires local webcam)
- Consider the web game version for cloud deployment
- Model files must be included (they are)

---

### Option 2: Heroku

#### Prerequisites:
```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### Files Needed:
1. `Procfile` (already created)
2. `runtime.txt` (already created)
3. `requirements.txt` (already exists)

#### Deployment Steps:
```bash
# Login to Heroku
heroku login

# Create new app
heroku create isl-communication-system

# Deploy
git push heroku main

# Open app
heroku open
```

---

### Option 3: Docker Deployment

#### Using Docker:
```bash
# Build image
docker build -t isl-system .

# Run container
docker run -p 8501:8501 isl-system
```

#### Using Docker Compose:
```bash
docker-compose up -d
```

---

### Option 4: Local Deployment

#### For Development/Testing:
```bash
# Activate virtual environment
.\\venv311\\Scripts\\activate

# Run Streamlit app
streamlit run streamlit-version/Home.py

# Or run web game
python web_game_version/server.py
```

---

## 🔧 CI/CD Pipeline

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:

1. **Code Quality**: Checks formatting with Black, isort, and Flake8
2. **Dependencies**: Verifies all packages install correctly
3. **Testing**: Runs test suite and syntax checks
4. **Security**: Scans for vulnerabilities
5. **Documentation**: Validates README and links
6. **Deployment Prep**: Creates deployment artifacts

### Workflow Triggers:
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual trigger via GitHub Actions UI

### View Workflow Status:
Visit: `https://github.com/Abs6187/ISL_MASTEK/actions`

---

## 📦 Deployment Checklist

Before deploying, ensure:

- [ ] All tests pass (`pytest tests/`)
- [ ] Dependencies are up to date
- [ ] Model files are committed
- [ ] Environment variables are set (if any)
- [ ] `.gitignore` excludes venv folders
- [ ] README is updated with deployment URL
- [ ] Team attribution is correct

---

## 🌐 Production URLs

After deployment, update these:

- **Streamlit App**: `https://[your-app].streamlit.app`
- **GitHub Repo**: `https://github.com/Abs6187/ISL_MASTEK`
- **Documentation**: Add to README.md

---

## 🔒 Environment Variables

If needed, set these in your deployment platform:

```bash
# For Streamlit Cloud: Settings > Secrets
# For Heroku: heroku config:set KEY=value

# Example (if using API keys):
# GROQ_API_KEY=your_key_here
# PERPLEXITY_API_KEY=your_key_here
```

---

## 📊 Monitoring

### Streamlit Cloud:
- Built-in analytics dashboard
- View logs in the "Manage app" section
- Resource usage monitoring

### Heroku:
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

---

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Ensure `requirements.txt` has all dependencies
   - Check Python version matches (3.11)

2. **Model Files Missing**
   - Verify model files are in `streamlit-version/assets/models/`
   - Check file sizes (should not be empty)

3. **Camera Not Working**
   - Cloud deployments cannot access local webcam
   - Use local deployment for camera features
   - Consider alternative input methods for cloud

4. **Memory Issues**
   - Models consume significant memory
   - Use appropriate instance size
   - Consider model optimization

---

## 📞 Support

**Team HII_1 - Mastek DeepBlue Season 11**

- Abhay Gupta: [LinkedIn](https://in.linkedin.com/in/abhay-gupta-197b17264)
- Bhumika Patel: [LinkedIn](https://www.linkedin.com/in/bhumika-patel-ml/)
- Kripanshu Gupta: [LinkedIn](https://in.linkedin.com/in/kripanshu-gupta-a66349261)
- Dipanshu Patel: [LinkedIn](https://www.linkedin.com/in/dipanshu-patel-080513243/)

**Mentor**: Sucheta Ranade

**Project**: Bridging Communication Gaps for the Hearing-Impaired in India

---

## 🎉 Quick Deploy Commands

```bash
# Test locally first
streamlit run streamlit-version/Home.py

# Run tests
pytest tests/ -v

# Check for issues
flake8 streamlit-version/ --max-line-length=120

# Deploy to Streamlit Cloud
# Just push to main branch and follow Streamlit Cloud UI steps
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

**Happy Deploying! 🚀**
