import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', html)
for i in imgs:
    if 'URL' in i or not (i.startswith('images/') or i.startswith('http') or i.startswith('data:')):
        print("Odd img src:", i)
