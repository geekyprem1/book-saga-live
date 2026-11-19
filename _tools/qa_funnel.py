#!/usr/bin/env python3
"""Verify the OTO funnel wiring: every page's no-thanks target exists,
and the chain runs oto1 -> ds1 -> oto2 -> ds2 -> ... -> oto5 -> ds5 -> home."""
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

chain = ["oto1.html", "ds1.html", "oto2.html", "ds2.html", "oto3.html",
         "ds3.html", "oto4.html", "ds4.html", "oto5.html", "ds5.html"]

print("%-10s %-14s %-8s %s" % ("page", "no-thanks ->", "exists", "buy configured"))
ok = True
for f in chain:
    h = open(f, encoding="utf-8").read()
    m = re.search(r'no:\s*"([^"]*)"', h)
    target = m.group(1) if m else "??"
    exists = os.path.exists(target)
    buy = re.search(r'buy:\s*"([^"]*)"', h)
    buy_url = buy.group(1) if buy else ""
    ok = ok and exists
    print("%-10s %-14s %-8s %s" % (f, target, "yes" if exists else "NO", buy_url or "(empty — needs checkout URL)"))

print()
print("chain intact" if ok else "BROKEN LINKS")
