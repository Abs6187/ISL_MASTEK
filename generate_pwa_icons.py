"""Generate all PWA icons from ai_mascot.png"""
import os
try:
    from PIL import Image
except ImportError:
    print('Install Pillow first: pip install Pillow')
    exit(1)

src = 'web_game_version/frontend/images/nano_banana.png'
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
    # Use mascot as mask if it has an alpha channel
    if mascot.mode in ('RGBA', 'LA') or (mascot.mode == 'P' and 'transparency' in mascot.info):
        canvas.paste(mascot, offset, mascot)
    else:
        canvas.paste(mascot, offset)
except ValueError:
    canvas.paste(mascot, offset)

canvas.save(os.path.join(out_dir, 'icon-maskable-512x512.png'))
print('✅ icon-maskable-512x512.png')

# 192x192 small icon (ai_mascot.png) replacement
mascot_path = os.path.join(os.path.dirname(out_dir), 'ai_mascot.png')
if os.path.exists(mascot_path):
    backup_path = os.path.join(os.path.dirname(out_dir), 'ai_mascot_backup.png')
    if not os.path.exists(backup_path):
        os.rename(mascot_path, backup_path)
        print(f'Original ai_mascot.png backed up to {backup_path}')

icon192 = img.resize((192, 192), Image.LANCZOS)
icon192.save(mascot_path)
print('✅ ai_mascot.png (192x192) updated with nano banana')

print('\n🎉 All PWA icons generated! Deploy and test.')
