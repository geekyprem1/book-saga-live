import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check img tags
img_srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
missing_imgs = []
found_imgs = 0
for s in img_srcs:
    # clean query string or anchor
    clean_path = s.split('?')[0].split('#')[0]
    if not clean_path.startswith('http'):
        if os.path.exists(clean_path):
            found_imgs += 1
        else:
            missing_imgs.append(s)

print(f"Images in <img>: Found {found_imgs}, Missing {len(missing_imgs)}")
if missing_imgs:
    for m in set(missing_imgs):
        print(f"  Missing: {m}")

# Check CSS urls
css_urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', html, re.I)
missing_css = []
found_css = 0
for s in css_urls:
    clean_path = s.split('?')[0].split('#')[0]
    if not clean_path.startswith('http') and not clean_path.startswith('data:'):
        if os.path.exists(clean_path):
            found_css += 1
        else:
            missing_css.append(s)

print(f"CSS url() assets: Found {found_css}, Missing {len(missing_css)}")
if missing_css:
    for m in set(missing_css):
        print(f"  Missing CSS asset: {m}")

# Check scripts
script_srcs = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
for s in script_srcs:
    clean_path = s.split('?')[0].split('#')[0]
    exists = os.path.exists(clean_path) if not clean_path.startswith('http') else 'Remote'
    print(f"Script: {s} -> Exists: {exists}")

# Check stylesheets
links = re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>', html, re.I)
for l in links:
    if 'stylesheet' in l.lower() or 'cdn.min.css' in l.lower():
        clean_path = l.split('?')[0].split('#')[0]
        exists = os.path.exists(clean_path) if not clean_path.startswith('http') else 'Remote'
        print(f"Link: {l} -> Exists: {exists}")

# Check PDFs
for pdf in ['f/part-1-the-third-daughter.pdf', 'f/part-2-the-mothers-secret.pdf', 'f/part-3-the-sister-who-lied.pdf']:
    if os.path.exists(pdf):
        print(f"PDF {pdf}: Exists ({os.path.getsize(pdf):,} bytes)")
    else:
        print(f"PDF {pdf}: MISSING!")
