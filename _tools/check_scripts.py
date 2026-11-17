import re

with open('raw_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Check for location/hostname checks
host_checks = re.findall(r'.{0,50}(?:location\.host|location\.hostname|document\.domain).{0,50}', html)
print(f"Host checks ({len(host_checks)}):")
for h in host_checks:
    print('  ', h.strip())

# Check for fetch / XMLHttpRequest / $.ajax / $.post / $.get
ajax_calls = re.findall(r'.{0,50}(?:\$\.ajax|\$\.get|\$\.post|fetch\(|XMLHttpRequest).{0,50}', html)
print(f"AJAX / fetch calls ({len(ajax_calls)}):")
for a in ajax_calls:
    print('  ', a.strip())

# Check for convertri API calls
cvt_api = re.findall(r'.{0,50}api\.convertri\.com.{0,50}', html)
print(f"Convertri API calls ({len(cvt_api)}):")
for c in cvt_api:
    print('  ', c.strip())

# Check for analytics / tracking
gtm = re.findall(r'GTM-[A-Z0-9]+', html)
print("GTM IDs:", set(gtm))
fbq = re.findall(r'fbq\(', html)
print("FB Pixel calls:", len(fbq))
