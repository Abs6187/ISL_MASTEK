# Signify PWA - Icon Generation Guide

## Required Icons

The PWA needs the following icon files to be fully installable on all devices:

| File | Size | Purpose | Location |
|------|------|---------|----------|
| `icon-512x512.png` | 512×512 px | App icon (required for install) | `frontend/images/icons/` |
| `icon-maskable-512x512.png` | 512×512 px | Adaptive icon (Android) | `frontend/images/icons/` |
| `ai_mascot.png` | 192×192 px | Small icon ✅ **Already exists** | `frontend/images/` |

## Step 1: Create the icons directory

```bash
mkdir -p web_game_version/frontend/images/icons
```

## Step 2: Generate the 512×512 icon

### Option A: Using the existing mascot image (recommended)

Resize `images/ai_mascot.png` to 512×512:

**Using Python (Pillow):**
```python
from PIL import Image

img = Image.open('web_game_version/frontend/images/ai_mascot.png')
img_resized = img.resize((512, 512), Image.LANCZOS)
img_resized.save('web_game_version/frontend/images/icons/icon-512x512.png')
print('✅ icon-512x512.png created')
```

**Using ImageMagick:**
```bash
convert images/ai_mascot.png -resize 512x512 images/icons/icon-512x512.png
```

**Using ffmpeg:**
```bash
ffmpeg -i images/ai_mascot.png -vf scale=512:512 images/icons/icon-512x512.png
```

### Option B: Online tools

1. **PWA Icon Generator**: https://www.pwabuilder.com/imageGenerator
   - Upload your source image (use `ai_mascot.png` or a custom design)
   - It generates all required sizes automatically

2. **Favicon.io**: https://favicon.io/
   - Upload image → download pack with all sizes

3. **RealFaviconGenerator**: https://realfavicongenerator.net/
   - Best for comprehensive icon pack (favicon, Apple touch, Android)

## Step 3: Generate the maskable icon

Maskable icons need **safe area padding** — the important content should be within the inner 80% circle.

### Option A: Manual with padding

```python
from PIL import Image, ImageDraw

# Create 512x512 canvas with the app's background color
canvas = Image.new('RGBA', (512, 512), (28, 26, 41, 255))  # #1c1a29

# Load and resize mascot to fit within safe area (80% = 410px)
mascot = Image.open('web_game_version/frontend/images/ai_mascot.png')
mascot = mascot.resize((360, 360), Image.LANCZOS)

# Center the mascot
offset = ((512 - 360) // 2, (512 - 360) // 2)
canvas.paste(mascot, offset, mascot if mascot.mode == 'RGBA' else None)
canvas.save('web_game_version/frontend/images/icons/icon-maskable-512x512.png')
print('✅ icon-maskable-512x512.png created')
```

### Option B: Maskable.app

1. Go to https://maskable.app/editor
2. Upload your icon
3. Adjust padding to fit the safe zone
4. Export as 512×512 PNG

## Step 4: Verify

After generating the icons:

```
web_game_version/frontend/
├── images/
│   ├── ai_mascot.png              ← 192×192 (already exists)
│   └── icons/
│       ├── icon-512x512.png       ← 512×512 (generate this)
│       └── icon-maskable-512x512.png  ← 512×512 maskable (generate this)
├── manifest.json                  ← references all icons
├── sw.js                          ← service worker
├── pwa.js                         ← PWA registration
└── offline.html                   ← offline fallback
```

## Step 5: Test the PWA

1. Deploy to Render (must be HTTPS for PWA to work)
2. Open Chrome DevTools → **Application** tab
3. Check:
   - **Manifest**: All fields should be green ✅
   - **Service Worker**: Should show "activated and running"
   - **Installability**: Should show no errors
4. Click the install icon in Chrome's address bar to install

## Quick Python Script (run from project root)

```python
"""Generate all PWA icons from ai_mascot.png"""
import os
try:
    from PIL import Image
except ImportError:
    print('Install Pillow first: pip install Pillow')
    exit(1)

src = 'web_game_version/frontend/images/ai_mascot.png'
out_dir = 'web_game_version/frontend/images/icons'
os.makedirs(out_dir, exist_ok=True)

img = Image.open(src)

# 512x512 regular icon
icon512 = img.resize((512, 512), Image.LANCZOS)
icon512.save(os.path.join(out_dir, 'icon-512x512.png'))
print('✅ icon-512x512.png')

# 512x512 maskable icon (with padding)
canvas = Image.new('RGBA', (512, 512), (28, 26, 41, 255))
mascot = img.resize((360, 360), Image.LANCZOS)
offset = ((512 - 360) // 2, (512 - 360) // 2)
try:
    canvas.paste(mascot, offset, mascot)
except ValueError:
    canvas.paste(mascot, offset)
canvas.save(os.path.join(out_dir, 'icon-maskable-512x512.png'))
print('✅ icon-maskable-512x512.png')

print('\n🎉 All PWA icons generated! Deploy and test.')
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No matching service worker detected" | Service worker must be at root (`/sw.js`) and served over HTTPS |
| "Manifest missing 512x512 icon" | Generate and place `icon-512x512.png` in `images/icons/` |
| App not installable | Ensure HTTPS + valid manifest + SW with fetch handler |
| Install button not appearing | The `beforeinstallprompt` event only fires when all criteria are met |
| Icons look cropped on Android | Use the maskable icon with proper safe area padding |
| Service worker not updating | Bump `CACHE_NAME` version in `sw.js` (e.g., `signify-v2`) |

## Cache Management

To update cached content after deploying new code:

1. Open `sw.js`
2. Change `CACHE_NAME` from `'signify-v1'` to `'signify-v2'`
3. Deploy — the new service worker will activate and purge old caches
