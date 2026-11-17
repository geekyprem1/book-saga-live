import re

with open('raw_page.html', 'r', encoding='utf-8') as f:
    raw = f.read()

matches = [m.start() for m in re.finditer(r'src=[\'"]URL[\'"]', raw)]
print(f"Occurrences of src='URL' in raw_page.html: {len(matches)}")
for idx in matches[:3]:
    print("--- Context ---")
    print(raw[max(0, idx - 100):min(len(raw), idx + 200)])
