import re

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

imgix_urls = set(re.findall(r'https://convertri\.imgix\.net/[^\'"\s)]+', html))
print(f"Total Convertri imgix URLs: {len(imgix_urls)}")
for u in sorted(imgix_urls):
    print(u)
