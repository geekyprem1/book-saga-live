import re

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

img_srcs = set(re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I))
print(f"Total img src unique: {len(img_srcs)}")
for s in sorted(img_srcs):
    print(s)
