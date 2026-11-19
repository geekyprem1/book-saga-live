#!/usr/bin/env python3
"""Structural QA for the generated OTO / downsell pages."""
import re
import os
import glob
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

files = sorted(glob.glob("oto*.html") + glob.glob("ds*.html"))
print("%-10s %-5s %-4s %-9s %-11s %s" % ("file", "secs", "h1", "lastSec", "links", "images"))

allok = True
for f in files:
    h = open(f, encoding="utf-8").read()
    secs = re.findall(r'<section[^>]*class="([^"]*)"', h)
    h1 = len(re.findall(r"<h1[ >]", h))
    last = secs[-1] if secs else ""
    decision_last = "bs-decision" in last

    links = set(re.findall(r'(?:href|data-no)="([^"#][^"]*)"', h))
    internal = {l for l in links if not l.startswith(("http", "mailto", "javascript"))}
    broken = sorted(l for l in internal if not os.path.exists(l))

    imgs = set(re.findall(r'<img[^>]+src="([^"]+)"', h))
    badimg = sorted(i for i in imgs if not os.path.exists(i))

    ok = decision_last and not broken and not badimg and h1 == 1 and len(secs) >= 10
    allok = allok and ok
    print("%-10s %-5d %-4d %-9s %-11s %s %s" % (
        f, len(secs), h1,
        "YES" if decision_last else "NO:" + last[:14],
        "ok" if not broken else "BROKEN:" + ",".join(broken),
        "ok" if not badimg else "MISSING:" + ",".join(badimg),
        "" if ok else "  <-- FAIL",
    ))

print()
print("ALL OK" if allok else "ISSUES FOUND")
sys.exit(0 if allok else 1)
