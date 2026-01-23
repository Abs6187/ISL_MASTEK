# ISL Test Suite

This directory contains comprehensive tests for the ISL Communication System.

## Test Files

### `test_basic.py`
Basic validation tests:
- Import checks
- Model file existence
- Syntax validation
- Requirements validation

### `test_cloud_deployment.py`
Cloud deployment specific tests:
- Audio fallback handling
- OpenCV headless mode
- System dependencies
- PyAudio optional handling
- Streamlit Cloud configuration

### `test_integration.py`
Integration tests:
- Full import chains
- Model loading and prediction
- Asset availability
- Cross-component compatibility

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_cloud_deployment.py -v
```

### Run with coverage:
```bash
pytest tests/ --cov=streamlit-version --cov=web_game_version --cov-report=html
```

### Run specific test class:
```bash
pytest tests/test_cloud_deployment.py::TestCloudDeployment -v
```

## Test Categories

### ✅ Cloud Compatibility Tests
- Audio device fallback
- OpenGL library availability
- PyAudio optional handling
- Headless OpenCV mode

### ✅ Code Quality Tests
- Python syntax validation
- Import compatibility
- File structure validation

### ✅ Deployment Tests
- Configuration file presence
- System packages specification
- Docker compatibility
- Requirements validation

### ✅ Functional Tests
- Model loading
- Asset availability
- API compatibility

## CI/CD Integration

These tests run automatically in GitHub Actions on every push. See `.github/workflows/ci-cd.yml` for the full pipeline.

## Local Development

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Run tests before commits:
```bash
pytest tests/ -v
```

## Test Coverage

Current coverage focuses on:
- Cloud deployment compatibility (critical for Streamlit Cloud)
- Model file validation
- Import chain verification
- Configuration validation

## Adding New Tests

When adding features, add corresponding tests:
1. Add test methods to appropriate test class
2. Follow naming convention: `test_<feature_name>`
3. Use descriptive docstrings
4. Handle missing files gracefully with `pytest.skip()`

## Troubleshooting

**Tests fail locally but pass in CI:**
- Check Python version (should be 3.11)
- Verify all dependencies installed
- Check for platform-specific issues

**Import errors:**
- Ensure you're in virtual environment
- Run `pip install -r requirements.txt`
- Check PYTHONPATH includes project root

**Model file tests skipped:**
- Large model files may not be in repository
- Tests will skip gracefully
- This is expected behavior
