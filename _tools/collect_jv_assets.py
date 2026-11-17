import re
import urllib.parse
import os
import hashlib

with open('raw_jv.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Scripts
scripts = set(re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

# 2. Stylesheets & fonts
links = set(re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I))
css_links = {l for l in links if 'stylesheet' in l or 'css' in l}
font_links = {l for l in links if 'font' in l}

# 3. Images in img tags
img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

# 4. CSS urls
css_urls = set(re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I))

# 5. Icons
icons = set(re.findall(r'<link[^>]+rel=[\'"][^\'"]*icon[^\'"]*[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I))

print(f"Scripts ({len(scripts)}):")
for s in scripts:
    print('  ', s)

print(f"\nCSS Links ({len(css_links)}):")
for c in css_links:
    print('  ', c)

print(f"\nFont Links ({len(font_links)}):")
for f in font_links:
    print('  ', f)

print(f"\nImages ({len(img_srcs)}):")
for i in sorted(img_srcs):
    print('  ', i)

print(f"\nCSS URLs ({len(css_urls)}):")
for c in sorted(css_urls):
    print('  ', c)
