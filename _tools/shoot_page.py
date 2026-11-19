#!/usr/bin/env python3
"""Screenshot a page tall, then crop vertical bands for review."""
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
src = sys.argv[1] if len(sys.argv) > 1 else "oto1.html"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
height = int(sys.argv[3]) if len(sys.argv) > 3 else 12000

tag = os.path.splitext(os.path.basename(src))[0]
full = os.path.join("_shots", "%s-full-%d.png" % (tag, width))

url = "file:///" + os.path.abspath(src).replace("\\", "/")
subprocess.run([
    CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=1",
    "--window-size=%d,%d" % (width, height),
    "--virtual-time-budget=9000",
    "--screenshot=" + os.path.abspath(full),
    url,
], capture_output=True)

if not os.path.exists(full):
    raise SystemExit("screenshot failed")

from PIL import Image
im = Image.open(full)
W, H = im.size
print("full:", W, "x", H)

band = 1400
n = 0
for top in range(0, H, band):
    bottom = min(top + band, H)
    crop = im.crop((0, top, W, bottom))
    if crop.getbbox() is None:
        continue
    out = os.path.join("_shots", "%s-%d-%d.png" % (tag, width, top))
    crop.save(out)
    n += 1
    print("band", top, "->", out)
print("bands:", n)
