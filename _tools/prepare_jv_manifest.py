import re
import os
import urllib.parse
import hashlib

with open('raw_jv.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Collect all media URLs
img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))
css_urls = set(re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I))
icon_srcs = set(re.findall(r'<link[^>]+href=[\'"](https://convertri\.imgix\.net/[^\'"]+)[\'"]', html, re.I))

media_urls = set()
for u in img_srcs:
    if u.startswith('http'):
        media_urls.add(u)
for u in css_urls:
    if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', 'imgix', 'convertri']):
        if not any(f in u for f in ['woff', 'ttf', 'eot', 'vimeo', 'google']):
            media_urls.add(u)
for u in icon_srcs:
    media_urls.add(u)

# Also check custom font: ccf0064f-0036-11f1-8caa-06d664cfaed9.otf
custom_fonts = set(re.findall(r'https://cdn\.convertri\.com/font/[^\'"\s)]+', html))
for f in custom_fonts:
    media_urls.add(f)

print(f"Total media/font URLs in JV page: {len(media_urls)}")

# Map each URL to a clean filename in images/ (or fonts/)
jv_media_map = {}
for u in sorted(media_urls):
    parsed = urllib.parse.urlparse(u)
    path = parsed.path
    orig_name = os.path.basename(urllib.parse.unquote(path))
    if not orig_name or '.' not in orig_name:
        orig_name = 'image.png'
    clean_name = re.sub(r'[^\w\-_\.]', '_', orig_name)
    name_root, ext = os.path.splitext(clean_name)
    if 'fm=png' in u:
        ext = '.png'
    elif 'fm=webp' in u:
        ext = '.webp'
    elif 'fm=jpg' in u or 'fm=jpeg' in u:
        ext = '.jpg'
    url_hash = hashlib.md5(u.encode('utf-8')).hexdigest()[:6]
    candidate = f"{name_root}_{url_hash}{ext}"
    if ext == '.otf':
        target = f"fonts/{clean_name}"
    else:
        target = f"images/{candidate}"
    jv_media_map[u] = target

# Check how many are already downloaded
already = 0
needed = {}
for u, local_path in jv_media_map.items():
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        already += 1
    else:
        needed[u] = local_path

print(f"Already downloaded: {already}")
print(f"Needed to download: {len(needed)}")
for u, p in needed.items():
    print(f"  Need: {p} <- {u}")

import json
with open('jv_manifest.json', 'w', encoding='utf-8') as f:
    json.dump({'all': jv_media_map, 'needed': needed}, f, indent=2)
