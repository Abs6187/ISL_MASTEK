# Bidirectional Indian Sign Language Recognition

A comprehensive system for translating Indian Sign Language (ISL) to speech/text and vice-versa, featuring a gamified learning module.

## 🚀 Features

*   **Sign Alphabet & Number Recognition**: Real-time detection of ISL signs using `mediapipe` and `scikit-learn`.
*   **Speech-to-Sign**: Converts spoken English into ISL sign animations.
*   **Text-to-Sign**: Visualizes typed text as ISL gestures.
*   **Gamified Learning**: A web-based game to learn and practice ISL signs with quizzes and leaderboards.

## 🛠️ Installation & Setup

**Prerequisites**:
*   **Python 3.11** (Required strictly for compatibility)
*   Webcam

### 1. Set up the Environment
Open a terminal in the project directory and create a virtual environment using Python 3.11:

```powershell
# Create venv w/ Python 3.11
py -3.11 -m venv venv311

# Activate the environment
.\venv311\Scripts\activate
```

### 2. Install Dependencies
Install the required packages. This project relies on specific versions to function correctly (`mediapipe==0.10.9`, `scikit-learn==1.6.0`, `protobuf<4`).

```powershell
pip install -r requirements.txt
```

---

## 🏃‍♂️ Usage

> **IMPORTANT**: Always run commands using `.\venv311\Scripts\python` to ensure you are using the correct environment. Using just `python` might use the wrong system version.

### 1. Run the Streamlit App (Translator)
This handles the core recognition and translation features.

```powershell
.\venv311\Scripts\python -m streamlit run streamlit-version/Home.py
```
> Access at: **http://localhost:8501** (or 8502 if 8501 is busy)

### 2. Run the Web Game
This launches the gamified learning platform.

```powershell
.\venv311\Scripts\python web_game_version/server.py
```
> Access at: **http://127.0.0.1:5000**

---

## 👨‍💻 Developer Resources

### Project Structure
*   `streamlit-version/`: Contains the main translation application code.
*   `web_game_version/`: Contains the Flask server and frontend for the game.
*   `web_game_version/server.py`: The backend API handling predictions.
*   `web_game_version/frontend/index.html`: The entry point for the web game.

### Common Issues & Fixes
*   **`AttributeError: module 'mediapipe' has no attribute 'solutions'`**:
    *   **Fix**: Ensure you are using `mediapipe==0.10.9`. Run `pip install mediapipe==0.10.9`.
*   **`ModuleNotFoundError: No module named 'sklearn'`** or **Pickle Errors**:
    *   **Fix**: Ensure `scikit-learn==1.6.0` is installed. Run `pip install scikit-learn==1.6.0`.
*   **NameError: name 'os' is not defined**:
    *   **Fix**: This has been resolved in the latest `server.py` update.

### API Usage
The Flask server exposes a prediction endpoint:
*   **POST** `/predict`
*   **Body**: `{"image": "base64_string", "category": "general"}`

---

## 👥 Credits

This project was created for **Mastek DeepBlue Season 11** ([https://deepblue.co.in/](https://deepblue.co.in/)) to address the problem statement: **"Bridging Communication Gaps for the Hearing-Impaired in India"**.

**Team:** HII_1  
**Mentor:** Sucheta Ranade

### Team Members
*   **Abhay Gupta** - [LinkedIn](https://in.linkedin.com/in/abhay-gupta-197b17264)
*   **Bhumika Patel** - [LinkedIn](https://www.linkedin.com/in/bhumika-patel-ml/)
*   **Kripanshu Gupta** - [LinkedIn](https://in.linkedin.com/in/kripanshu-gupta-a66349261)
*   **Dipanshu Patel** - [LinkedIn](https://www.linkedin.com/in/dipanshu-patel-080513243/)
