import os
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('jv_manifest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

needed = data['needed']
print(f"Downloading {len(needed)} files...")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://bookseriesai.com/jv',
}

def download_item(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True, url, local_path, os.path.getsize(local_path), "Already exists"
    
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                content = resp.read()
                with open(local_path, 'wb') as f:
                    f.write(content)
                return True, url, local_path, len(content), "OK"
        except Exception as e:
            time.sleep(1 + attempt)
            err = str(e)
    return False, url, local_path, 0, err

success = 0
failed = []

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(download_item, url, path): (url, path) for url, path in needed.items()}
    for f in as_completed(futures):
        ok, url, path, size, msg = f.result()
        if ok:
            success += 1
            print(f"[OK] ({size:,} B) {path}")
        else:
            failed.append((url, path, msg))
            print(f"[FAIL] {url} -> {msg}")

print(f"\nDownload finished. Success: {success}/{len(needed)}. Failed: {len(failed)}")
