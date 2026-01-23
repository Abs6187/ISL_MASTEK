import streamlit as st
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*InconsistentVersionWarning.*')

# Set dark theme with Material UI color schema
st.set_page_config(
    page_title="Bidirectional Sign Language Communication System", 
    page_icon="🖐️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Material UI-inspired Color Schema
# Primary: Deep Purple/Indigo (#5E35B1, #3F51B5)
# Secondary: Cyan/Teal (#00BCD4, #00ACC1, #4FC3F7)
# Background: Dark (#0E1117, #1E1E1E, #262730)
# Text: Light (#FAFAFA, #E0E0E0)

st.markdown("""
    <style>
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0E1117 0%, #1a1d29 50%, #262730 100%);
        }
        
        /* Main Container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Title Styles */
        .title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 50%, #00BCD4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #B0BEC5;
            font-weight: 400;
            margin-bottom: 2rem;
        }
        
        /* Section Cards with Material Design */
        .section {
            padding: 24px;
            border-radius: 12px;
            background: linear-gradient(145deg, #1E1E1E 0%, #262730 100%);
            margin-bottom: 20px;
            border: 1px solid rgba(94, 53, 177, 0.1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3), 
                        0 1px 3px rgba(94, 53, 177, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .section:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.4), 
                        0 2px 6px rgba(94, 53, 177, 0.2);
            border-color: rgba(94, 53, 177, 0.3);
        }
        
        .section h3 {
            color: #00BCD4;
            font-weight: 600;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .section h5 {
            color: #4FC3F7;
            font-weight: 500;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .section p {
            color: #E0E0E0;
            line-height: 1.7;
            font-size: 1rem;
        }
        
        .section ul, .section ol {
            color: #E0E0E0;
            line-height: 1.8;
        }
        
        .section li {
            margin-bottom: 0.5rem;
        }
        
        .section a {
            color: #4FC3F7;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .section a:hover {
            color: #00BCD4;
            text-decoration: underline;
        }
        
        .section code {
            background-color: #262730;
            color: #4FC3F7;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        
        .section pre {
            background-color: #0E1117;
            border: 1px solid #3F51B5;
            border-radius: 8px;
            padding: 16px;
            color: #E0E0E0;
            overflow-x: auto;
            margin: 12px 0;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E1E1E 0%, #262730 100%);
            border-right: 1px solid rgba(94, 53, 177, 0.2);
        }
        
        [data-testid="stSidebar"] .css-1d391kg {
            color: #E0E0E0;
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #5E35B1 0%, #3F51B5 100%);
            color: #FAFAFA;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(94, 53, 177, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #4527A0 0%, #303F9F 100%);
            box-shadow: 0 4px 8px rgba(94, 53, 177, 0.5);
            transform: translateY(-1px);
        }
        
        /* Text Color */
        p, span, li {
            color: #E0E0E0;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #FAFAFA;
        }
        
        /* Image Captions */
        .stImage > div {
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 8px;
            border: 1px solid rgba(0, 188, 212, 0.2);
        }
        
        /* Accent Highlights */
        b, strong {
            color: #4FC3F7;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Homepage Content

st.markdown("<h1 class='title'>Bidirectional Sign Language Communication System</h1>", unsafe_allow_html=True)
st.markdown("<h5 class='subtitle'>Breaking Barriers Between Sign Language Users and Non-Signers</h5><br>", unsafe_allow_html=True)

st.write(
    """
    Welcome to the Bidirectional Sign Language Communication System—an innovative application designed to facilitate seamless, real-time communication between individuals who use sign language and those who rely on spoken or written language. Our system leverages advanced technologies to provide accurate and efficient translations, promoting inclusivity and understanding.
    """
)

# # Placeholder for logo/image
# st.image("C:\\Users\\Mohammed Mudasir\\OneDrive\\Desktop\\Mini_Project\\Streamlit\\assets\\logo\\ISL.jpg", use_container_width=True)  

# Introduction Section
st.markdown("""
            <div class='section'><h3> Brief Overview</h3><p>The Bidirectional Sign Language Communication System is an innovative application designed to bridge the communication gap between individuals who use sign language and those who rely on spoken or written language. By leveraging advanced technologies such as computer vision, machine learning, and natural language processing, the system facilitates seamless, real-time translation in both directions: from sign language to speech/text and vice versa.<br>
            <br>In the <b>Sign-to-Speech/Text</b> mode, the system captures hand gestures using a camera, processes these inputs to recognize specific signs, and then converts them into corresponding spoken words or text. Conversely, in the <b>Speech/Text-to-Sign</b> mode, the application takes spoken or written language as input and translates it into sign language, displaying the appropriate gestures visually. This bidirectional functionality ensures effective communication, promoting inclusivity and understanding between sign language users and non-signers.<br>
            <br> The application is designed with user-friendliness in mind, featuring an intuitive interface that allows users to select their preferred mode of communication easily. Its real-time processing capabilities ensure that conversations flow naturally, without significant delays. By providing a tool that accommodates both sign language and spoken/written language, the system aims to foster more inclusive interactions across diverse communication preferences.
            </p></div>
            """, unsafe_allow_html=True)

# How It Works
st.markdown("<div class='section'><h3>⚙️ How It Works</h3><ul><li>Signers can gesture, and the system will translate them into text and speech.</li><li>Non-signers can speak or enter text, and the system will generate the corresponding sign visuals.</li></ul></div>", unsafe_allow_html=True)

# How to Use
st.markdown("<div class='section'><h3>📌 How to Use</h3><ol><li>Select <b>Sign Alphabet Recognition</b> to translate sign language alphabets to speech.</li><li>Select <b>Sign Number Recognition</b> to translate sign language numbers to speech.</li><li>Select <b>Speech-to-Sign Translation</b> to convert speech into signs.</li><li>Select <b>Text-to-Sign Translation</b> to convert speech into signs.</li></ol></div>", unsafe_allow_html=True)

# Model & Technology
st.markdown("<div class='section'><h3>🧠 Model & Technology</h3><p>This system employs machine learning models that utilize <b>hand landmarks</b> for recognizing sign language gestures. It incorporates a <b>Multi-layer Perceptron (MLP) Classifier</b>, enabling accurate interpretation of both sign alphabets and numbers. The system facilitates <b>real-time translation</b> of sign language into speech and text, while also converting speech and text into corresponding sign gestures. By employing <b>deep learning</b> techniques and advanced classification methods, this application aims to enhance communication accessibility for the deaf and hard of hearing, bridging the gap in everyday</p></div>", unsafe_allow_html=True)

# Developer Resources (Examples)
st.markdown("""
<div class='section'>
    <h3>👨‍💻 Developer Resources</h3>
    <p>This section provides examples for developers who want to understand the underlying logic or interact with the API.</p>
    
    <h5>1. Flask API Example (Prediction)</h5>
    <p>Send a POST request to <code>/predict</code> with a base64 encoded image.</p>
    <pre>
curl -X POST http://localhost:5000/predict \\
     -H "Content-Type: application/json" \\
     -d '{"image": "data:image/jpeg;base64,..."}'
    </pre>

    <h5>2. Speech-to-Sign Logic</h5>
    <p>The system listens for speech and filters for alphabets.</p>
    <pre>
# Python Logic
text = recognizer.recognize_google(audio)
alphabets_only = re.sub(r'[^a-zA-Z]', '', text)
    </pre>
    
    <h5>3. Visual Examples</h5>
    <p>Below are examples of the dataset used for training the ISL models.</p>
</div>
""", unsafe_allow_html=True)

import os
# Display images side-by-side
col1, col2, col3, col4 = st.columns(4)
img_dir = os.path.join(os.path.dirname(__file__), 'assets', 'images')

with col1:
    st.image(os.path.join(img_dir, "A.jpg"), caption="Letter A")
with col2:
    st.image(os.path.join(img_dir, "B.JPG"), caption="Letter B")
with col3:
    st.image(os.path.join(img_dir, "5.JPG"), caption="Number 5")
with col4:
    st.image(os.path.join(img_dir, "9.JPG"), caption="Number 9")

# Contact & Credits
st.markdown("""
<div class='section'>
    <h3>Credits</h3>
    <p>
        This project was created for <b>Mastek DeepBlue Season 11</b> (<a href="https://deepblue.co.in/" target="_blank" style="color: #4FC3F7;">deepblue.co.in</a>) 
        to address the problem statement: <b>"Bridging Communication Gaps for the Hearing-Impaired in India"</b>.
    </p>
    <h5>Team: <b>HII_1</b></h5>
    <h5>Mentor: <b>Sucheta Ranade</b></h5>
    <h5>Team Members</h5>
    <ul>
        <li><b>Abhay Gupta</b> - <a href="https://in.linkedin.com/in/abhay-gupta-197b17264" target="_blank" style="color: #4FC3F7;">LinkedIn</a></li>
        <li><b>Bhumika Patel</b> - <a href="https://www.linkedin.com/in/bhumika-patel-ml/" target="_blank" style="color: #4FC3F7;">LinkedIn</a></li>
        <li><b>Kripanshu Gupta</b> - <a href="https://in.linkedin.com/in/kripanshu-gupta-a66349261" target="_blank" style="color: #4FC3F7;">LinkedIn</a></li>
        <li><b>Dipanshu Patel</b> - <a href="https://www.linkedin.com/in/dipanshu-patel-080513243/" target="_blank" style="color: #4FC3F7;">LinkedIn</a></li>
    </ul>
</div>
""", unsafe_allow_html=True)
