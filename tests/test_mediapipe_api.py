"""
Tests to verify mediapipe.solutions.hands (legacy API) will work correctly
on Streamlit Cloud with the pinned mediapipe==0.10.9 version.

Context:
 - mediapipe >= 0.10.14 removed mp.solutions entirely.
 - mediapipe.tasks (Tasks API, current) requires libEGL.so.1 which
   is absent on headless cloud servers → OSError crash.
 - mediapipe == 0.10.9 still has mp.solutions.hands AND does NOT
   require libEGL, so we pin to that version in requirements.txt.

If running locally on a newer mediapipe, version-sensitive tests are skipped.
"""
import sys
import os
import pytest


def _get_mp_version():
    try:
        import mediapipe as mp
        return tuple(int(x) for x in mp.__version__.split(".")[:3])
    except ImportError:
        return None


PINNED_VERSION = (0, 10, 9)
LOCAL_VERSION = _get_mp_version()
CORRECT_VERSION = LOCAL_VERSION == PINNED_VERSION if LOCAL_VERSION else False

# Marker to skip tests that require the exact pinned version
skip_if_wrong_version = pytest.mark.skipif(
    not CORRECT_VERSION,
    reason=(
        f"Local mediapipe is {'.'.join(str(x) for x in LOCAL_VERSION) if LOCAL_VERSION else 'not installed'}; "
        f"these tests target pinned mediapipe==0.10.9 on Streamlit Cloud. "
        "Run: pip install mediapipe==0.10.9 to test locally."
    )
)


def test_mediapipe_importable():
    """mediapipe must be importable in any environment."""
    import mediapipe as mp
    assert mp.__version__, "mediapipe not properly installed"
    print(f"✅ mediapipe {mp.__version__} is installed")


def test_requirements_pins_mediapipe():
    """
    Verify requirements.txt pins mediapipe to exactly 0.10.9.
    This is critical — any other version may lack mp.solutions.hands.
    """
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_path), "requirements.txt not found"
    content = open(req_path).read()
    assert 'mediapipe==0.10.9' in content, (
        "requirements.txt must pin mediapipe==0.10.9 exactly.\n"
        "Found: " + [l for l in content.splitlines() if 'mediapipe' in l.lower()] [0]
        if any('mediapipe' in l for l in content.splitlines()) else "No mediapipe line found"
    )
    print("✅ requirements.txt correctly pins mediapipe==0.10.9")


def test_mediapipe_tasks_api_NOT_used():
    """
    Verify mediapipe.tasks (Tasks API requiring libEGL) is NOT imported
    in either recognition page. This works regardless of local mediapipe version.
    """
    pages_dir = os.path.join(os.path.dirname(__file__), '..', 'streamlit-version', 'pages')

    offending = []
    for fname in ['1_Sign_Alphabet_Recognition.py', '2_Sign_Number_Recognition.py']:
        fpath = os.path.join(pages_dir, fname)
        if not os.path.exists(fpath):
            continue
        content = open(fpath).read()
        if 'from mediapipe.tasks' in content or 'mediapipe.tasks.python' in content:
            offending.append(fname)

    assert not offending, (
        f"These files still import mediapipe.tasks (requires libEGL on headless servers): {offending}\n"
        "Replace with mp.solutions.hands.Hands() instead."
    )
    print("✅ mediapipe.tasks (Tasks API) correctly removed from recognition pages")


def test_mp_solutions_hands_usage_in_pages():
    """
    Verify both recognition pages use mp.solutions.hands (the correct legacy API).
    """
    pages_dir = os.path.join(os.path.dirname(__file__), '..', 'streamlit-version', 'pages')

    for fname in ['1_Sign_Alphabet_Recognition.py', '2_Sign_Number_Recognition.py']:
        fpath = os.path.join(pages_dir, fname)
        if not os.path.exists(fpath):
            pytest.fail(f"{fname} not found")
        content = open(fpath).read()
        assert 'mp.solutions.hands' in content, (
            f"{fname} does not use mp.solutions.hands — required for EGL-free operation"
        )
        assert 'mp_hands.Hands(' in content, (
            f"{fname} does not instantiate mp_hands.Hands() — check the VideoProcessor.__init__"
        )
        assert 'hands.process(' in content, (
            f"{fname} does not call hands.process() — check the recv() method"
        )
        assert 'multi_hand_landmarks' in content, (
            f"{fname} does not use multi_hand_landmarks — check classic API result format"
        )
        print(f"✅ {fname}: correctly uses mp.solutions.hands API")


@skip_if_wrong_version
def test_solutions_hands_module_exists():
    """Verify mp.solutions.hands module is importable (only on pinned version)."""
    import mediapipe as mp
    assert hasattr(mp, 'solutions'), "mp.solutions missing"
    assert hasattr(mp.solutions, 'hands'), "mp.solutions.hands missing"
    print("✅ mp.solutions.hands module exists")


@skip_if_wrong_version
def test_hands_class_is_uppercase():
    """Verify Hands() class uses uppercase H (guards against issue #5410 mistake)."""
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    assert hasattr(mp_hands, 'Hands'), "mp.solutions.hands.Hands class missing"
    print("✅ mp.solutions.hands.Hands (uppercase) confirmed")


@skip_if_wrong_version
def test_hands_instantiates_without_egl():
    """Verify Hands() works without libEGL (the core OS fix)."""
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    try:
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.3,
        )
        hands.close()
        print("✅ mp.solutions.hands.Hands() instantiated — no libEGL required")
    except OSError as e:
        if 'libEGL' in str(e) or 'libGLES' in str(e):
            raise AssertionError(f"EGL dependency triggered on legacy API: {e}")
        raise


@skip_if_wrong_version
def test_hands_processes_blank_frame():
    """Full pipeline test: process a dummy frame with no hands."""
    import mediapipe as mp
    import numpy as np
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    with mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2) as hands:
        result = hands.process(dummy)
        assert result.multi_hand_landmarks is None
    print("✅ hands.process() ran on blank frame — no crash")


if __name__ == "__main__":
    # When run directly, show clear status
    version_str = '.'.join(str(x) for x in LOCAL_VERSION) if LOCAL_VERSION else "unknown"
    print(f"Local mediapipe: {version_str} | Pinned for Cloud: 0.10.9")
    if not CORRECT_VERSION:
        print("⚠️  Version-sensitive tests will be SKIPPED (run on Streamlit Cloud or install mediapipe==0.10.9)")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pytest', __file__, '-v'])
