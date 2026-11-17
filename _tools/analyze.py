import re
import urllib.parse

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

title_m = re.search(r'<title>(.*?)</title>', html, re.I)
print('Title:', title_m.group(1) if title_m else 'None')

css_links = re.findall(r'<link[^>]+>', html, re.I)
print(f'Link tags ({len(css_links)}):')
for l in css_links:
    if 'stylesheet' in l.lower() or 'font' in l.lower():
        print('  ', l)

style_tags = re.findall(r'<style[^>]*>([\s\S]*?)</style>', html, re.I)
print(f'Inline <style> tags count: {len(style_tags)}')
total_style_len = sum(len(s) for s in style_tags)
print(f'Total inline CSS length: {total_style_len} bytes')

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', html, re.I)
print(f'External scripts ({len(scripts)}):')
for s in scripts:
    print('  ', s)

imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
print(f'Img src count: {len(imgs)}')
img_domains = set()
for img in imgs:
    parsed = urllib.parse.urlparse(img)
    if parsed.netloc:
        img_domains.add(parsed.netloc)
print('Image domains:', img_domains)

# Background images in CSS
bg_imgs = re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I)
print(f'CSS url() count: {len(bg_imgs)}')
bg_domains = set()
for bg in bg_imgs:
    parsed = urllib.parse.urlparse(bg)
    if parsed.netloc:
        bg_domains.add(parsed.netloc)
print('CSS url domains:', bg_domains)

iframes = re.findall(r'<iframe[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
print(f'Iframes ({len(iframes)}):')
for ifr in iframes:
    print('  ', ifr)
