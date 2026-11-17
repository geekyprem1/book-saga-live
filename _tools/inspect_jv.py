import re
import urllib.parse

with open('raw_jv.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

title_m = re.search(r'<title>(.*?)</title>', html, re.I)
print('Title:', title_m.group(1) if title_m else 'None')

# Check links
links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>([\s\S]*?)</a>', html, re.I)
print(f'Total links: {len(links)}')
unique_hrefs = {}
for href, text in links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if href not in unique_hrefs:
        unique_hrefs[href] = clean_text[:60]

print('Unique links:')
for href, txt in unique_hrefs.items():
    print(f'  {href} -> {txt}')

# Check external scripts
scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
print(f'External scripts ({len(scripts)}):')
for s in scripts:
    print('  ', s)

# Check iframes
iframes = re.findall(r'<iframe[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
print(f'Iframes ({len(iframes)}):')
for ifr in iframes:
    print('  ', ifr)

# Check images
img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))
css_urls = set(re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I))
print(f'Unique <img> srcs: {len(img_srcs)}')
print(f'Unique CSS urls: {len(css_urls)}')
