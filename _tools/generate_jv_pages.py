import re
import os
import json

with open('raw_jv.html', 'r', encoding='utf-8', errors='ignore') as f:
raw_path = os.path.join(os.path.dirname(__file__), 'raw_jv.html') if not os.path.exists('raw_jv.html') else 'raw_jv.html'
manifest_path = os.path.join(os.path.dirname(__file__), 'jv_manifest.json') if not os.path.exists('jv_manifest.json') else 'jv_manifest.json'

with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

with open('jv_manifest.json', 'r', encoding='utf-8') as f:
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

media_map = manifest['all']

# Scripts & CSS map
scripts_map = {
    'https://cdn.convertri.com/jquery-1.12.2.min.js?v=2026-09-16-13-12-03': 'js/jquery-1.12.2.min.js',
    'https://cdn.convertri.com/jquery-1.12.2.min.js': 'js/jquery-1.12.2.min.js',
    'https://cdn.convertri.com/hls.min.js?v=2026-09-16-13-12-03': 'js/hls.min.js',
    'https://cdn.convertri.com/hls.min.js': 'js/hls.min.js',
    'https://cdn.convertri.com/cdn.min.css?v=2026-09-16-13-12-03': 'css/cdn.min.css',
    'https://cdn.convertri.com/cdn.min.css': 'css/cdn.min.css',
    'https://cdn.convertri.com/font-awesome/font-awesome.woff2?v=4.7.0': 'fonts/font-awesome.woff2',
    'https://cdn.convertri.com/font-awesome/font-awesome.woff2': 'fonts/font-awesome.woff2',
    'https://cdn.convertri.com/font/ccf0064f-0036-11f1-8caa-06d664cfaed9.otf': 'fonts/ccf0064f-0036-11f1-8caa-06d664cfaed9.otf',
}

# Generate root jv.html
jv_root = content

# Replace scripts & CSS
for url, local in scripts_map.items():
    jv_root = jv_root.replace(url, local)

# Replace all media
for url, local in media_map.items():
    jv_root = jv_root.replace(url, local)
    jv_root = jv_root.replace(url.replace('&', '&amp;'), local)
    alt = url.replace('%2C', ',')
    jv_root = jv_root.replace(alt, local)
    jv_root = jv_root.replace(alt.replace('&', '&amp;'), local)

# Clean up msapplication icons
jv_root = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=150&(?:amp;)?fm=png',
    'images/Icon_e1d6c3.png',
    jv_root
)
jv_root = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?h=150&(?:amp;)?fm=png',
    'images/Icon_3e5072.png',
    jv_root
)
jv_root = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?fm=png',
    'images/Icon_3e5072.png',
    jv_root
)

# Better title if needed
if '<title>JV Page</title>' in jv_root:
    jv_root = jv_root.replace('<title>JV Page</title>', '<title>BookSeries AI - Official JV & Affiliate Page ($5,000 Prizes)</title>')

VIDEO_URL = 'https://videotourl.com/videos/1791388333158-c8eab52f-65a8-42e9-83e1-a4162b84e928.mp4'

# Replace video in root jv.html
jv_root = jv_root.replace(VIDEO_URL, 'videos/demo.mp4')

with open('jv.html', 'w', encoding='utf-8') as f:
    f.write(jv_root)

print("Generated jv.html successfully.")

# Now generate jv/index.html with relative ../ prefix
os.makedirs('jv', exist_ok=True)

jv_sub = content

# Replace video in jv/index.html
jv_sub = jv_sub.replace(VIDEO_URL, '../videos/demo.mp4')

for url, local in scripts_map.items():
    jv_sub = jv_sub.replace(url, f"../{local}")

for url, local in media_map.items():
    sub_local = f"../{local}"
    jv_sub = jv_sub.replace(url, sub_local)
    jv_sub = jv_sub.replace(url.replace('&', '&amp;'), sub_local)
    alt = url.replace('%2C', ',')
    jv_sub = jv_sub.replace(alt, sub_local)
    jv_sub = jv_sub.replace(alt.replace('&', '&amp;'), sub_local)

jv_sub = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=150&(?:amp;)?fm=png',
    '../images/Icon_e1d6c3.png',
    jv_sub
)
jv_sub = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?h=150&(?:amp;)?fm=png',
    '../images/Icon_3e5072.png',
    jv_sub
)
jv_sub = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?fm=png',
    '../images/Icon_3e5072.png',
    jv_sub
)

if '<title>JV Page</title>' in jv_sub:
    jv_sub = jv_sub.replace('<title>JV Page</title>', '<title>BookSeries AI - Official JV & Affiliate Page ($5,000 Prizes)</title>')

with open('jv/index.html', 'w', encoding='utf-8') as f:
    f.write(jv_sub)

print("Generated jv/index.html successfully.")
