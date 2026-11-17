import re
import os
import urllib.parse
from asset_manifest import PDFS, SCRIPTS, CSS_FILES, FONTS, MEDIA_MAP

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace PDF links and iframes
# e.g., https://bookseriesai.com/f/part-1-the-third-daughter.pdf#page=1&zoom=page-width -> f/part-1-the-third-daughter.pdf#page=1&zoom=page-width
for url, local_path in PDFS.items():
    content = content.replace(url, local_path)

# Replace scripts
for url, local_path in SCRIPTS.items():
    content = content.replace(url, local_path)

# Replace CSS
for url, local_path in CSS_FILES.items():
    content = content.replace(url, local_path)

# Replace fonts
for url, local_path in FONTS.items():
    content = content.replace(url, local_path)

# Replace all media images (img src, css url, icons)
for url, local_path in MEDIA_MAP.items():
    # Direct replace
    content = content.replace(url, local_path)
    # Also handle html-encoded url (e.g. &amp; instead of &)
    html_encoded = url.replace('&', '&amp;')
    content = content.replace(html_encoded, local_path)
    # Also handle unencoded query params
    # e.g. %2C vs ,
    alt_url = url.replace('%2C', ',')
    content = content.replace(alt_url, local_path)
    alt_url_enc = alt_url.replace('&', '&amp;')
    content = content.replace(alt_url_enc, local_path)

# Also clean up msapplication meta logos to local icon
content = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=150&(?:amp;)?fm=png',
    'images/Icon_e1d6c3.png',
    content
)
content = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?h=150&(?:amp;)?fm=png',
    'images/Icon_3e5072.png',
    content
)
content = re.sub(
    r'https://convertri\.imgix\.net/[^\'"]*Icon\.png\?auto=compress%2Cformat&(?:amp;)?fit=clip&(?:amp;)?w=310&(?:amp;)?fm=png',
    'images/Icon_3e5072.png',
    content
)

# Fix title if it's just 'FE'
if '<title>FE</title>' in content:
    content = content.replace('<title>FE</title>', '<title>Book Series AI - Live Special Offer</title>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated index.html successfully with local asset references.")
