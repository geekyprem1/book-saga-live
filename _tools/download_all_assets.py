import os
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from asset_manifest import PDFS, SCRIPTS, CSS_FILES, FONTS, MEDIA_MAP

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://bookseriesai.com/live',
}

all_downloads = {}
all_downloads.update(SCRIPTS)
all_downloads.update(CSS_FILES)
all_downloads.update(FONTS)
all_downloads.update(MEDIA_MAP)
all_downloads.update(PDFS)

print(f"Total files to download: {len(all_downloads)}")

def download_item(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True, url, local_path, os.path.getsize(local_path), "Already exists"
    
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                with open(local_path, 'wb') as f:
                    f.write(data)
                return True, url, local_path, len(data), "OK"
        except Exception as e:
            time.sleep(1 + attempt)
            err = str(e)
    return False, url, local_path, 0, err

success_count = 0
failed = []

start_time = time.time()
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_item, url, path): (url, path) for url, path in all_downloads.items()}
    for f in as_completed(futures):
        ok, url, path, size, msg = f.result()
        if ok:
            success_count += 1
            print(f"[OK] ({size:,} B) {path}")
        else:
            failed.append((url, path, msg))
            print(f"[FAIL] {url} -> {msg}")

elapsed = time.time() - start_time
print(f"\nDone in {elapsed:.1f}s. Success: {success_count}/{len(all_downloads)}. Failed: {len(failed)}")
if failed:
    print("Failed downloads:")
    for url, path, msg in failed:
        print(f"  {url} -> {msg}")
