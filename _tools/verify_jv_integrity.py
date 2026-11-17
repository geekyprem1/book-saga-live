import re
import os

def check_file(filepath, base_dir='.'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    img_srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.I)
    missing = []
    found = 0
    for s in img_srcs:
        clean = s.split('?')[0].split('#')[0]
        if not clean.startswith('http'):
            target = os.path.normpath(os.path.join(base_dir, clean))
            if os.path.exists(target):
                found += 1
            else:
                missing.append(s)
    
    css_urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', html, re.I)
    missing_css = []
    found_css = 0
    for s in css_urls:
        clean = s.split('?')[0].split('#')[0]
        if not clean.startswith('http') and not clean.startswith('data:') and not clean.startswith('#') and not clean.startswith('%23'):
            target = os.path.normpath(os.path.join(base_dir, clean))
            if os.path.exists(target):
                found_css += 1
            else:
                missing_css.append(s)
    
    print(f"[{filepath}]")
    print(f"  Images: Found {found}, Missing {len(missing)}")
    if missing:
        for m in set(missing):
            print(f"    Missing: {m}")
    print(f"  CSS urls: Found {found_css}, Missing {len(missing_css)}")
    if missing_css:
        for m in set(missing_css):
            print(f"    Missing CSS: {m}")

check_file('jv.html', '.')
check_file('jv/index.html', 'jv')
