import re
import json

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Let's inspect links
links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>([\s\S]*?)</a>', html, re.I)
print(f'Total links: {len(links)}')
unique_hrefs = {}
for href, text in links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if href not in unique_hrefs:
        unique_hrefs[href] = clean_text[:50]

print('Unique link hrefs:')
for href, txt in unique_hrefs.items():
    print(f'  {href} -> {txt}')

# Check for forms
forms = re.findall(r'<form[^>]*>([\s\S]*?)</form>', html, re.I)
print(f'Total forms: {len(forms)}')

# Check for timer
timers = re.findall(r'timer|countdown', html, re.I)
print(f'Timer/countdown occurrences: {len(timers)}')

# Check Convertri scripts / config
cvt_data = re.findall(r'convertri|cvtPageData|window\._cvt', html, re.I)
print(f'Convertri occurrences: {len(cvt_data)}')
