### Install Dependencies and Pre-commit Hooks

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Installs project dependencies using 'uv sync' and sets up pre-commit hooks for code quality management.

```bash
# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install
```

--------------------------------

### Basic Streamlit-WebRTC Setup

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Demonstrates the minimal configuration required to start video and audio streaming in a Streamlit application. It highlights the mandatory 'key' argument for the webrtc_streamer component.

```python
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="sample")
```

```shell
$ streamlit run app.py
```

--------------------------------

### Run Development Server

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Instructions to start the frontend development server and the main Streamlit application for local development. Requires setting a flag in component.py.

```bash
# Set _RELEASE = False in streamlit_webrtc/component.py (development only, don't commit)

# Start frontend dev server
cd streamlit_webrtc/frontend
pnpm dev

# In another terminal, run the main app
streamlit run home.py
```

--------------------------------

### Install streamlit-webrtc

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Command to install the streamlit-webrtc library using pip.

```shell
$ pip install -U streamlit-webrtc

```

--------------------------------

### Install Dependencies with uv

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Installs project dependencies using the `uv` package manager. This command synchronizes the environment based on the project's configuration files, ensuring all necessary packages are present.

```shell
$ uv sync
```

--------------------------------

### Format All Code

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Runs the make command to format all code across the project.

```makefile
# Format all code
make format
```

--------------------------------

### Build Complete Package

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Builds the entire streamlit-webrtc package, including both frontend and backend components.

```makefile
# Build the complete package (frontend + backend)
make build
```

--------------------------------

### Build Frontend Only

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Builds only the frontend assets for the streamlit-webrtc component.

```bash
# Frontend build only
cd streamlit_webrtc/frontend
pnpm run build
```

--------------------------------

### Format Frontend Code

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Formats the frontend code using pnpm's formatting script.

```bash
# Format frontend code
cd streamlit_webrtc/frontend
pnpm format
```

--------------------------------

### Install Pre-commit Hooks

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Sets up pre-commit hooks for the project. This command integrates the pre-commit framework, which helps automate code quality checks and formatting before each commit.

```shell
$ pre-commit install
```

--------------------------------

### Run Streamlit Application

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Starts the Streamlit application. This command executes the `home.py` script, serving the Python-based web application for local testing and development.

```shell
$ streamlit run home.py
```

--------------------------------

### Run Frontend Development Server

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Navigates to the frontend directory and starts the development server using `pnpm`. This is crucial for frontend development and testing, allowing for live reloading and debugging.

```shell
cd streamlit_webrtc/frontend
$ pnpm dev
```

--------------------------------

### Perform Type Checking

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Runs static type checking on the Python codebase using mypy.

```bash
# Type checking
uv run mypy .
```

--------------------------------

### Release Patch, Minor, or Major Version

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Commands to automate the release process by incrementing the version and creating necessary artifacts.

```makefile
# Use `make release/patch`, `make release/minor`, or `make release/major`
# CI/CD automatically builds and publishes on tag push
```

--------------------------------

### Format and Check Backend Code

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Applies code formatting and checks for style issues in the Python backend code using Ruff.

```bash
# Format backend code
# Or individually:
uv run ruff format .
uv run ruff check . --fix
```

--------------------------------

### Run Python and Frontend Tests

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/CLAUDE.md

Executes Python tests using pytest and frontend tests using pnpm test within their respective directories.

```bash
# Run Python tests
uv run pytest

# Run frontend tests
cd streamlit_webrtc/frontend
pnpm test
```

--------------------------------

### Video Frame Processing with Callback

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Shows how to process video frames in real-time by providing a callback function to the webrtc_streamer. This example flips the video frame vertically using PyAV library's VideoFrame.

```python
from streamlit_webrtc import webrtc_streamer
import av

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:]

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
```

--------------------------------

### Streamlit-WebRTC API Changes and Deprecations

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Details changes in the streamlit-webrtc API, focusing on the transition from `VideoTransformerBase` to `VideoProcessorBase` and updated arguments for `webrtc_streamer`. This section guides users on migrating from versions prior to v0.20.0.

```APIDOC
API Changes (Versions <0.20 to >=0.20):

Class/Method Renaming & Signature Changes:
- `VideoTransformerBase` is deprecated.
- `VideoTransformerBase.transform()` is deprecated.
- Use `VideoProcessorBase` instead of `VideoTransformerBase`.
- Use `VideoProcessorBase.recv()` instead of `VideoTransformerBase.transform()`.
- The `recv` method must return an instance of `av.VideoFrame` or `av.AudioFrame`.

`webrtc_streamer()` Argument Changes:
- `video_transformer_factory` argument is deprecated.
- Use `video_processor_factory` instead of `video_transformer_factory`.
- `async_transform` argument is deprecated.
- Use `async_processing` instead of `async_transform`.

Note: The API is not finalized and may change without backward compatibility until v1.0.
```

--------------------------------

### Build Project Package

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Executes the build process for the project package. This command is used locally for development and testing, and is also run automatically during the release process in CI/CD.

```makefile
make build
```

--------------------------------

### Set Next Release Version

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Updates the project version and creates a Git tag for a new release using `bump-my-version`. This command automates version bumping, tagging, and committing, preparing the project for deployment.

```shell
$ uv run bump-my-version bump <version> --tag --commit --commit-args='--allow-empty' --verbose
```

--------------------------------

### SSL Proxy for Local Development

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

This shell command sequence demonstrates how to use an SSL proxy to serve a Streamlit application over HTTPS locally. It's useful for testing HTTPS requirements without deploying to a full remote server. The proxy forwards requests from a specified HTTPS port to the Streamlit app's HTTP port.

```shell
streamlit run your_app.py  # Assume your app is running on http://localhost:8501
# Then, after downloading the binary from the GitHub page above to ./ssl-proxy,
./ssl-proxy -from 0.0.0.0:8000 -to 127.0.0.1:8501  # Proxy the HTTP page from port 8501 to port 8000 via HTTPS
# Then access https://localhost:8000
```

--------------------------------

### Configure Twilio TURN Server for WebRTC

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Demonstrates how to use the Twilio API to obtain ICE server information for WebRTC. This configuration is crucial for media streaming in restrictive network environments. It involves fetching tokens and passing the `ice_servers` to the `webrtc_streamer` function.

```python
## This sample code is from https://www.twilio.com/docs/stun-turn/api
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

token = client.tokens.create()

# Then, pass the ICE server information to webrtc_streamer().
webrtc_streamer(
    # ...
    rtc_configuration={
        "iceServers": token.ice_servers
    }
    # ...
)
```

--------------------------------

### Push Changes and Tags to GitHub

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/DEVELOPMENT.md

Pushes local commits and Git tags to the remote GitHub repository. This action triggers the CI/CD pipeline for automatic deployment of the new release.

```shell
$ git push
$ git push --tags
```

--------------------------------

### Configure STUN Server for Remote Deployment

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

This Python code snippet shows how to configure the STUN server for the `webrtc_streamer` function. Setting the `rtc_configuration` with a STUN server URL is essential for establishing WebRTC media streaming connections when the application is deployed on remote hosts or accessed by peers behind NATs.

```python
webrtc_streamer(
    # ...
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
    # ...
)
```

--------------------------------

### Configure Streamlit-WebRTC Logging Levels

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Shows how to set log levels for the `streamlit_webrtc` library and its internal dependencies like `aioice`. This allows control over the verbosity of logs, which is useful for debugging and monitoring.

```python
st_webrtc_logger = logging.getLogger("streamlit_webrtc")
st_webrtc_logger.setLevel(logging.WARNING)
```

```python
aioice_logger = logging.getLogger("aioice")
aioice_logger.setLevel(logging.WARNING)
```

--------------------------------

### Passing Parameters to Video Callback

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Illustrates how to pass dynamic parameters from the Streamlit UI to the video frame processing callback. A checkbox is used to control whether the video frame is flipped or not.

```python
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av


flip = st.checkbox("Flip")


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:] if flip else img

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
```

--------------------------------

### PyAV VideoFrame API Reference

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Provides details on the PyAV library's VideoFrame object, which is used for handling video frames in callbacks. It covers methods for converting frames to NumPy arrays and creating frames from arrays, essential for video processing.

```APIDOC
av.VideoFrame:
  Description: Represents a video frame.
  Methods:
    to_ndarray(format: str) -> numpy.ndarray:
      Converts the frame to a NumPy array.
      Parameters:
        format: The desired pixel format (e.g., "bgr24", "rgb24").
      Returns: A NumPy array representing the video frame.
    from_ndarray(ndarray: numpy.ndarray, format: str) -> av.VideoFrame:
      Creates a VideoFrame from a NumPy array.
      Parameters:
        ndarray: The input NumPy array.
        format: The pixel format of the input array (e.g., "bgr24").
      Returns: An av.VideoFrame instance.
  Related Libraries:
    - PyAV: https://pyav.org/
    - NumPy: https://numpy.org/
```

--------------------------------

### Thread-Safe Data Sharing from Callback

Source: https://github.com/whitphx/streamlit-webrtc/blob/main/README.md

Demonstrates a pattern for safely sharing data (processed video frames) from a background callback thread to the main Streamlit script. It uses threading.Lock and a shared container for thread-safe access and processing, such as calculating image histograms.

```python
import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt

from streamlit_webrtc import webrtc_streamer

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame


ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ax.cla()
    ax.hist(gray.ravel(), 256, [0, 256])
    fig_place.pyplot(fig)
```

=== COMPLETE CONTENT === This response contains all available snippets from this library. No additional content exists. Do not make further requests.