import re
import urllib.parse

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Images in <img> tags
img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

# 2. CSS url()
css_urls = set(re.findall(r'url\([\'"]?(https?://[^\'")]+)[\'"]?\)', html, re.I))

# 3. Scripts
script_srcs = set(re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))

# 4. Stylesheets
style_srcs = set(re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I))
# also check reversed attributes
style_srcs.update(re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]stylesheet[\'"]', html, re.I))

# 5. PDFs and other links
pdf_links = set(re.findall(r'https?://[^\'"\s>]+\.pdf', html, re.I))

# 6. Icons
icon_links = set(re.findall(r'<link[^>]+rel=[\'"][^\'"]*icon[^\'"]*[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html, re.I))

print(f"Unique <img> srcs: {len(img_srcs)}")
print(f"Unique CSS urls: {len(css_urls)}")
print(f"Unique Script srcs: {len(script_srcs)}")
print(f"Unique Style srcs: {len(style_srcs)}")
print(f"Unique PDFs: {len(pdf_links)}")
print(f"Unique Icons: {len(icon_links)}")

all_assets = set()
all_assets.update(img_srcs)
all_assets.update(css_urls)
all_assets.update(script_srcs)
all_assets.update(style_srcs)
all_assets.update(pdf_links)
all_assets.update(icon_links)

print(f"Total unique assets: {len(all_assets)}")

# Let's filter external hostnames
domains = {}
for u in all_assets:
    parsed = urllib.parse.urlparse(u)
    domains[parsed.netloc] = domains.get(parsed.netloc, 0) + 1

for domain, count in sorted(domains.items(), key=lambda x: -x[1]):
    print(f"  {domain}: {count}")
