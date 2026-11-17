import re
import os
import urllib.parse
import hashlib

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Directories to create
for d in ['f', 'images', 'css', 'js', 'fonts']:
    os.makedirs(d, exist_ok=True)

# 1. PDFs
pdfs = {
    'https://bookseriesai.com/f/part-1-the-third-daughter.pdf': 'f/part-1-the-third-daughter.pdf',
    'https://bookseriesai.com/f/part-2-the-mothers-secret.pdf': 'f/part-2-the-mothers-secret.pdf',
    'https://bookseriesai.com/f/part-3-the-sister-who-lied.pdf': 'f/part-3-the-sister-who-lied.pdf',
}

# 2. JS
scripts = {
    'https://cdn.convertri.com/jquery-1.12.2.min.js?v=2026-10-22-08-26-37': 'js/jquery-1.12.2.min.js',
    'https://cdn.convertri.com/jquery-1.12.2.min.js': 'js/jquery-1.12.2.min.js',
    'https://cdn.convertri.com/hls.min.js?v=2026-10-22-08-26-37': 'js/hls.min.js',
    'https://cdn.convertri.com/hls.min.js': 'js/hls.min.js',
}

# 3. CSS
css_files = {
    'https://cdn.convertri.com/cdn.min.css?v=2026-10-22-08-26-37': 'css/cdn.min.css',
    'https://cdn.convertri.com/cdn.min.css': 'css/cdn.min.css',
}

# 4. Fonts
fonts = {
    'https://cdn.convertri.com/font-awesome/font-awesome.woff2?v=4.7.0': 'fonts/font-awesome.woff2',
    'https://cdn.convertri.com/font-awesome/font-awesome.woff2': 'fonts/font-awesome.woff2',
}

# 5. Extract all images and css urls
# Images in img src
img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

# CSS urls
css_urls = set(re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I))

# Favicon and icons
icon_srcs = set(re.findall(r'<link[^>]+href=[\'"](https://convertri\.imgix\.net/[^\'"]+)[\'"]', html, re.I))

# Aggregate all image/media URLs
media_urls = set()
for u in img_srcs:
    if u.startswith('http'):
        media_urls.add(u)
for u in css_urls:
    if any(u.lower().endswith(ext) or ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', 'imgix', 'convertri']):
        if not any(f in u for f in ['woff', 'ttf', 'eot', 'vimeo']):
            media_urls.add(u)
for u in icon_srcs:
    media_urls.add(u)

print(f"Total media/image URLs to download: {len(media_urls)}")

# Map each media URL to a clean filename in images/
media_map = {}
used_names = set()

for u in sorted(media_urls):
    parsed = urllib.parse.urlparse(u)
    path = parsed.path
    # Extract base filename from path
    orig_name = os.path.basename(urllib.parse.unquote(path))
    if not orig_name or '.' not in orig_name:
        orig_name = 'image.png'
    
    # Strip invalid windows chars
    clean_name = re.sub(r'[^\w\-_\.]', '_', orig_name)
    
    # Handle extensions and query parameters
    name_root, ext = os.path.splitext(clean_name)
    if 'fm=png' in u:
        ext = '.png'
    elif 'fm=webp' in u:
        ext = '.webp'
    elif 'fm=jpg' in u or 'fm=jpeg' in u:
        ext = '.jpg'
    
    # Hash the full URL for uniqueness if collisions
    url_hash = hashlib.md5(u.encode('utf-8')).hexdigest()[:6]
    candidate = f"{name_root}_{url_hash}{ext}"
    media_map[u] = f"images/{candidate}"

print(f"Generated {len(media_map)} media mappings.")

with open('asset_manifest.py', 'w', encoding='utf-8') as f:
    f.write(f"PDFS = {repr(pdfs)}\n")
    f.write(f"SCRIPTS = {repr(scripts)}\n")
    f.write(f"CSS_FILES = {repr(css_files)}\n")
    f.write(f"FONTS = {repr(fonts)}\n")
    f.write(f"MEDIA_MAP = {repr(media_map)}\n")

print("Saved asset_manifest.py successfully.")
