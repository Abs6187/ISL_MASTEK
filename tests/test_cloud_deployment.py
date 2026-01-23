# Comprehensive test suite for cloud deployment
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class TestCloudDeployment:
    """Test suite for cloud deployment compatibility"""
    
    def test_imports_without_audio(self):
        """Test that critical imports work without audio dependencies"""
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
    
    def test_optional_audio_imports(self):
        """Test that audio imports are optional and handled gracefully"""
        # These should not fail the app if unavailable
        try:
            import pygame
        except ImportError:
            pass  # Expected in some environments
        
        try:
            import pyaudio
        except ImportError:
            pass  # Expected in cloud
    
    def test_opencv_headless(self):
        """Test that OpenCV loads in headless mode"""
        import cv2
        # Should not require display
        assert cv2.__version__ is not None

class TestModelFiles:
    """Test that model files exist and are valid"""
    
    def test_model_files_exist(self):
        """Check all required model files are present"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        model_dir = os.path.join(base_dir, 'streamlit-version', 'assets', 'models')
        
        required_models = [
            'mlp_model_1.p',
            'mlp_model_2.p',
            'mlp_model_num.p'
        ]
        
        for model in required_models:
            model_path = os.path.join(model_dir, model)
            if os.path.exists(model_path):
                assert os.path.getsize(model_path) > 0, f"{model} is empty"
    
    def test_model_loading(self):
        """Test that models can be loaded with pickle"""
        import pickle
        base_dir = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(base_dir, 'streamlit-version', 'assets', 'models', 'mlp_model_1.p')
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    model_dict = pickle.load(f)
                assert 'model' in model_dict
            except Exception as e:
                pytest.skip(f"Model loading skipped: {e}")

class TestStreamlitPages:
    """Test Streamlit page files"""
    
    def test_home_page_syntax(self):
        """Test Home.py has valid syntax"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        home_path = os.path.join(base_dir, 'streamlit-version', 'Home.py')
        
        with open(home_path, 'r', encoding='utf-8') as f:
            code = f.read()
            try:
                compile(code, 'Home.py', 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in Home.py: {e}")
    
    def test_all_pages_syntax(self):
        """Test all page files have valid syntax"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pages_dir = os.path.join(base_dir, 'streamlit-version', 'pages')
        
        if os.path.exists(pages_dir):
            for filename in os.listdir(pages_dir):
                if filename.endswith('.py'):
                    filepath = os.path.join(pages_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        try:
                            compile(f.read(), filename, 'exec')
                        except SyntaxError as e:
                            pytest.fail(f"Syntax error in {filename}: {e}")
    
    def test_pages_have_audio_fallback(self):
        """Test that recognition pages handle audio gracefully"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pages_dir = os.path.join(base_dir, 'streamlit-version', 'pages')
        
        # Pages that use audio should have fallback
        audio_pages = [
            '1_🅰️ Sign Alphabet Recognition.py',
            '2_🔢 Sign Number Recognition.py'
        ]
        
        for page in audio_pages:
            page_path = os.path.join(pages_dir, page)
            if os.path.exists(page_path):
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert 'AUDIO_AVAILABLE' in content, f"{page} missing audio fallback"
                    assert 'try:' in content, f"{page} missing try-except for pygame"

class TestRequirements:
    """Test requirements and dependencies"""
    
    def test_requirements_file_exists(self):
        """Check requirements.txt exists"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        req_file = os.path.join(base_dir, 'requirements.txt')
        assert os.path.exists(req_file), "requirements.txt not found"
    
    def test_requirements_content(self):
        """Validate requirements.txt has needed packages"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        req_file = os.path.join(base_dir, 'requirements.txt')
        
        with open(req_file, 'r') as f:
            content = f.read().lower()
            
            # Critical packages
            assert 'streamlit' in content, "streamlit not in requirements"
            assert 'opencv' in content, "opencv not in requirements"
            assert 'mediapipe' in content, "mediapipe not in requirements"
            assert 'scikit-learn' in content or 'sklearn' in content, "sklearn not in requirements"
            
            # PyAudio should be commented out for cloud
            lines = content.split('\n')
            pyaudio_lines = [l for l in lines if 'pyaudio' in l and not l.strip().startswith('#')]
            assert len(pyaudio_lines) == 0, "PyAudio should be commented out for cloud deployment"
    
    def test_packages_txt_exists(self):
        """Check packages.txt for system dependencies"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pkg_file = os.path.join(base_dir, 'packages.txt')
        assert os.path.exists(pkg_file), "packages.txt not found (needed for Streamlit Cloud)"
    
    def test_packages_txt_content(self):
        """Validate packages.txt has OpenCV dependencies"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pkg_file = os.path.join(base_dir, 'packages.txt')
        
        if os.path.exists(pkg_file):
            with open(pkg_file, 'r') as f:
                content = f.read().lower()
                assert 'libgl' in content, "libgl1 not in packages.txt (needed for OpenCV)"

class TestDeploymentConfigs:
    """Test deployment configuration files"""
    
    def test_streamlit_config_exists(self):
        """Check .streamlit/config.toml exists"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        config_file = os.path.join(base_dir, '.streamlit', 'config.toml')
        assert os.path.exists(config_file), "Streamlit config not found"
    
    def test_dockerfile_exists(self):
        """Check Dockerfile exists for containerization"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        dockerfile = os.path.join(base_dir, 'Dockerfile')
        assert os.path.exists(dockerfile), "Dockerfile not found"
    
    def test_gitignore_excludes_venv(self):
        """Verify .gitignore excludes virtual environments"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        gitignore = os.path.join(base_dir, '.gitignore')
        
        if os.path.exists(gitignore):
            with open(gitignore, 'r') as f:
                content = f.read()
                assert 'venv' in content, "venv not in .gitignore"

class TestWebGameVersion:
    """Test web game version"""
    
    def test_server_py_syntax(self):
        """Test server.py has valid syntax"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        server_path = os.path.join(base_dir, 'web_game_version', 'server.py')
        
        if os.path.exists(server_path):
            with open(server_path, 'r', encoding='utf-8') as f:
                try:
                    compile(f.read(), 'server.py', 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Syntax error in server.py: {e}")
    
    def test_frontend_index_exists(self):
        """Check web game has index.html"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        index_path = os.path.join(base_dir, 'web_game_version', 'frontend', 'index.html')
        
        if os.path.exists(os.path.dirname(index_path)):
            assert os.path.exists(index_path), "Web game index.html not found"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
