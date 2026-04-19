"""
Tests to verify mediapipe.solutions.hands (legacy API) is available
and works correctly without requiring libEGL/libGLES.

This validates the fix for the OSError: libEGL.so.1 crash on
Streamlit Cloud (headless Linux, no GPU/display hardware).

Pinned: mediapipe==0.10.9 (last version with mp.solutions.hands support)
"""
import sys
import importlib
import numpy as np


def test_mediapipe_version_is_pinned():
    """Ensure mediapipe is pinned to a version that has mp.solutions.hands."""
    import mediapipe as mp
    version = tuple(int(x) for x in mp.__version__.split(".")[:3])
    # mp.solutions.hands exists in 0.10.0 - 0.10.9; removed in 0.10.14+
    assert version <= (0, 10, 9), (
        f"mediapipe {mp.__version__} is too new — mp.solutions.hands may be removed. "
        "Pin to mediapipe==0.10.9 in requirements.txt"
    )
    print(f"✅ mediapipe version OK: {mp.__version__}")


def test_solutions_hands_module_exists():
    """Verify mp.solutions.hands module is importable (not removed)."""
    import mediapipe as mp
    assert hasattr(mp, 'solutions'), "mediapipe has no 'solutions' attribute"
    assert hasattr(mp.solutions, 'hands'), (
        "mp.solutions has no 'hands' attribute — "
        "mediapipe version too new, pin to ==0.10.9"
    )
    print("✅ mp.solutions.hands module exists")


def test_hands_class_is_uppercase():
    """
    Verify the correct class name is Hands() (uppercase), not hands() (lowercase).
    The GitHub issue #5410 was caused by calling mpHands.hands() instead of mpHands.Hands().
    """
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    # Should have 'Hands' class (uppercase)
    assert hasattr(mp_hands, 'Hands'), (
        "mp.solutions.hands has no 'Hands' class — check mediapipe version"
    )
    # Should NOT be called as lowercase
    assert not hasattr(mp_hands, 'hands') or callable(getattr(mp_hands, 'hands', None)) is False, (
        "Do not call mp.solutions.hands.hands() (lowercase) — use Hands() (uppercase)"
    )
    print("✅ mp.solutions.hands.Hands (uppercase) class confirmed")


def test_hands_instantiates_without_egl():
    """
    Verify mp.solutions.hands.Hands() instantiates without requiring libEGL.
    This is the core fix — old Tasks API (vision.HandLandmarker) crashed with
    OSError: libEGL.so.1 on headless servers.
    """
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    try:
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3,
        )
        hands.close()
        print("✅ mp.solutions.hands.Hands() instantiated successfully (no EGL required)")
    except OSError as e:
        if "libEGL" in str(e) or "libGLES" in str(e):
            raise AssertionError(
                f"EGL/GLES dependency still triggered: {e}\n"
                "The mp.solutions.hands API should NOT require libEGL."
            )
        raise


def test_hands_processes_blank_frame():
    """
    Verify the full inference pipeline: construct Hands, run process() on a dummy frame.
    Ensures no runtime EGL crash happens during actual inference.
    """
    import mediapipe as mp
    import numpy as np

    mp_hands = mp.solutions.hands
    # 480x640 blank RGB image
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5,
    ) as hands:
        result = hands.process(dummy_frame)
        # On a blank frame, no hands should be detected
        assert result.multi_hand_landmarks is None
        print("✅ hands.process() ran successfully on blank frame (no crash)")


def test_mediapipe_tasks_api_NOT_used():
    """
    Ensure the mediapipe.tasks.python.vision.HandLandmarker (new C++ Tasks API)
    is NOT imported in our recognition pages — it requires libEGL.so on headless servers.
    """
    import ast, os
    pages_dir = os.path.join(
        os.path.dirname(__file__),
        '..', 'streamlit-version', 'pages'
    )
    bad_pattern_tasks = 'mediapipe.tasks'
    bad_pattern_vision = 'from mediapipe.tasks.python import vision'

    offending_files = []
    for fname in ['1_Sign_Alphabet_Recognition.py', '2_Sign_Number_Recognition.py']:
        fpath = os.path.join(pages_dir, fname)
        if not os.path.exists(fpath):
            continue
        content = open(fpath).read()
        if bad_pattern_tasks in content or bad_pattern_vision in content:
            offending_files.append(fname)

    assert not offending_files, (
        f"These files still import mediapipe.tasks (requires libEGL): {offending_files}\n"
        "Replace with mp.solutions.hands.Hands() instead."
    )
    print("✅ No mediapipe.tasks imports found in recognition pages")


if __name__ == "__main__":
    test_mediapipe_version_is_pinned()
    test_solutions_hands_module_exists()
    test_hands_class_is_uppercase()
    test_hands_instantiates_without_egl()
    test_hands_processes_blank_frame()
    test_mediapipe_tasks_api_NOT_used()
    print("\n✅ All mediapipe API tests passed!")
