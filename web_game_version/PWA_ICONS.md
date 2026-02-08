# Signify PWA - Icon Status & Guide

## ✅ Current Icon Status — All Generated

All PWA icons have been generated from `images/ai_mascot_backup.png` (1024×1024 source) and are in place:

| File | Size | Purpose | Location | Status |
|------|------|---------|----------|--------|
| `icon-48x48.png` | 48×48 px | Small icon | `frontend/images/icons/` | ✅ Generated |
| `icon-72x72.png` | 72×72 px | Medium icon | `frontend/images/icons/` | ✅ Generated |
| `icon-144x144.png` | 144×144 px | Large icon | `frontend/images/icons/` | ✅ Generated |
| `icon-192x192.png` | 192×192 px | PWA icon (required) | `frontend/images/icons/` | ✅ Generated |
| `icon-512x512.png` | 512×512 px | Splash screen (required) | `frontend/images/icons/` | ✅ Generated |
| `icon-maskable-192x192.png` | 192×192 px | Adaptive icon (Android) | `frontend/images/icons/` | ✅ Generated |
| `icon-maskable-512x512.png` | 512×512 px | Adaptive icon (Android) | `frontend/images/icons/` | ✅ Generated |
| `apple-touch-icon.png` | 180×180 px | iOS home screen icon | `frontend/images/icons/` | ✅ Generated |
| `favicon.ico` | 16/32/48 px | Browser tab icon | `frontend/` | ✅ Generated |
| `ai_mascot.png` | 192×192 px | Original mascot image | `frontend/images/` | ✅ Existing |
| `ai_mascot_backup.png` | 1024×1024 px | Source image for generation | `frontend/images/` | ✅ Existing |

## File Structure

```
web_game_version/frontend/
├── favicon.ico                            ← Browser tab icon (16/32/48)
├── manifest.json                          ← References all icons
├── sw.js                                  ← Service worker (caches icons)
├── pwa.js                                 ← PWA registration + install prompt
├── offline.html                           ← Offline fallback page
└── images/
    ├── ai_mascot.png                      ← 192×192 (original)
    ├── ai_mascot_backup.png               ← 1024×1024 (source)
    └── icons/
        ├── icon-48x48.png                 ← 48×48
        ├── icon-72x72.png                 ← 72×72
        ├── icon-144x144.png               ← 144×144
        ├── icon-192x192.png               ← 192×192
        ├── icon-512x512.png               ← 512×512
        ├── icon-maskable-192x192.png      ← 192×192 (with safe zone padding)
        ├── icon-maskable-512x512.png      ← 512×512 (with safe zone padding)
        └── apple-touch-icon.png           ← 180×180 (iOS)
```

## Regenerating Icons

If you update the mascot image, regenerate all icons from the 1024×1024 source:

```python
"""Regenerate all PWA icons from ai_mascot_backup.png"""
from PIL import Image
import os

src = Image.open('web_game_version/frontend/images/ai_mascot_backup.png').convert('RGBA')
out_dir = 'web_game_version/frontend/images/icons'
os.makedirs(out_dir, exist_ok=True)

# Standard icons
for size in [48, 72, 144, 192, 512]:
    icon = src.resize((size, size), Image.LANCZOS)
    icon.save(os.path.join(out_dir, f'icon-{size}x{size}.png'))
    print(f'icon-{size}x{size}.png')

# Maskable icons (content in inner 80%, background fill)
for size in [192, 512]:
    canvas = Image.new('RGBA', (size, size), (106, 17, 203, 255))  # #6a11cb
    inner = int(size * 0.75)
    small = src.resize((inner, inner), Image.LANCZOS)
    offset = (size - inner) // 2
    canvas.paste(small, (offset, offset), small if small.mode == 'RGBA' else None)
    canvas.save(os.path.join(out_dir, f'icon-maskable-{size}x{size}.png'))
    print(f'icon-maskable-{size}x{size}.png')

# Apple touch icon (180x180)
apple = src.resize((180, 180), Image.LANCZOS)
apple.save(os.path.join(out_dir, 'apple-touch-icon.png'))
print('apple-touch-icon.png')

# Favicon
fav16 = src.resize((16, 16), Image.LANCZOS)
fav16.save('web_game_version/frontend/favicon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48)])
print('favicon.ico')

print('\nAll icons regenerated!')
```

## Testing the PWA

1. Deploy to Render (must be HTTPS for PWA to work)
2. Open Chrome DevTools → **Application** tab
3. Check:
   - **Manifest**: All fields should be green ✅
   - **Service Worker**: Should show "activated and running"
   - **Installability**: Should show no errors
4. Click the install icon in Chrome's address bar to install

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No matching service worker detected" | SW must be at root (`/sw.js`) and served over HTTPS |
| "Manifest missing 512x512 icon" | Check `manifest.json` references `images/icons/icon-512x512.png` |
| App not installable | Ensure HTTPS + valid manifest + SW with fetch handler |
| Install button not appearing | `beforeinstallprompt` only fires when all criteria are met |
| Icons look cropped on Android | Maskable icons have safe area padding built in |
| Service worker not updating | Bump `CACHE_NAME` version in `sw.js` (currently `signify-v2`) |

## Cache Management

To update cached content after deploying new code:

1. Open `sw.js`
2. Change `CACHE_NAME` from `'signify-v2'` to `'signify-v3'` (increment version)
3. Deploy — the new service worker will activate and purge old caches
