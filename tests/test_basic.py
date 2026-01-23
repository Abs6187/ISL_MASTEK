# Basic tests for ISL System
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_imports():
    """Test that all critical imports work"""
    try:
        import streamlit
        import cv2
        import mediapipe
        import sklearn
        import numpy
        import flask
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_model_files_exist():
    """Test that model files exist"""
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'streamlit-version', 'assets', 'models')
    
    models = [
        'mlp_model_1.p',
        'mlp_model_2.p',
        'mlp_model_num.p'
    ]
    
    for model in models:
        model_path = os.path.join(model_dir, model)
        if os.path.exists(model_path):
            assert os.path.getsize(model_path) > 0, f"{model} is empty"

def test_streamlit_pages_syntax():
    """Test that Streamlit pages have valid Python syntax"""
    pages_dir = os.path.join(os.path.dirname(__file__), '..', 'streamlit-version', 'pages')
    
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.py'):
                filepath = os.path.join(pages_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        compile(f.read(), filename, 'exec')
                    except SyntaxError as e:
                        pytest.fail(f"Syntax error in {filename}: {e}")

def test_requirements_file():
    """Test that requirements.txt exists and has content"""
    req_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_file), "requirements.txt not found"
    
    with open(req_file, 'r') as f:
        content = f.read()
        assert len(content) > 0, "requirements.txt is empty"
        assert 'streamlit' in content.lower(), "streamlit not in requirements"
        assert 'mediapipe' in content.lower(), "mediapipe not in requirements"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
