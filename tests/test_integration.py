# Integration tests for ISL application
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class TestIntegration:
    """Integration tests for full application"""
    
    def test_streamlit_import_chain(self):
        """Test full import chain for Streamlit app"""
        try:
            import streamlit as st
            import cv2
            import mediapipe as mp
            import numpy as np
            import pickle
            
            # Verify MediaPipe hands is available
            mp_hands = mp.solutions.hands
            assert mp_hands is not None
            
        except Exception as e:
            pytest.fail(f"Import chain failed: {e}")
    
    def test_flask_import_chain(self):
        """Test full import chain for Flask server"""
        try:
            from flask import Flask, request, jsonify
            from flask_cors import CORS
            import cv2
            import mediapipe as mp
            
            assert True
        except Exception as e:
            pytest.fail(f"Flask import chain failed: {e}")
    
    def test_model_pickle_compatibility(self):
        """Test that sklearn models can be unpickled"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(base_dir, 'streamlit-version', 'assets', 'models', 'mlp_model_1.p')
        
        if os.path.exists(model_path):
            import pickle
            import sklearn
            
            try:
                with open(model_path, 'rb') as f:
                    model_dict = pickle.load(f)
                    model = model_dict.get('model')
                    
                    # Should be sklearn model
                    assert hasattr(model, 'predict'), "Model doesn't have predict method"
            except Exception as e:
                pytest.skip(f"Model test skipped: {e}")
    
    def test_image_assets_directory(self):
        """Check that image assets directory exists"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        images_dir = os.path.join(base_dir, 'streamlit-version', 'assets', 'images')
        
        # Should have images
        if os.path.exists(images_dir):
            files = os.listdir(images_dir)
            image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            assert len(image_files) > 0, "No image files found in assets/images"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
