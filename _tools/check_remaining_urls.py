import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find remaining http/https urls
urls = re.findall(r'https?://[^\s\'"<>)]+', content)
print(f"Total remaining http/https URLs: {len(urls)}")

# Group by domain
domains = {}
for u in urls:
    m = re.match(r'https?://([^/]+)', u)
    if m:
        d = m.group(1)
        domains[d] = domains.get(d, 0) + 1

for d, count in sorted(domains.items(), key=lambda x: -x[1]):
    print(f"  {d}: {count}")

# Check bookseriesai.com
bs_urls = [u for u in urls if 'bookseriesai.com' in u]
print("\nbookseriesai.com URLs:")
for u in bs_urls:
    print('  ', u)
unconverted = [u for u in urls if 'convertri' in u or 'bookseriesai.com/f/' in u]
print(f"\nUnconverted asset URLs ({len(unconverted)}):")
for u in unconverted[:20]:
    print('  ', u)
