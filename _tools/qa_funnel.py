#!/usr/bin/env python3
"""Verify the OTO funnel wiring: each offer's "no thanks" target exists and
the chain runs oto1 -> oto2 -> oto3 -> oto4 -> oto5 -> index.html.
There are no downsell pages by design."""
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

chain = ["oto1.html", "oto2.html", "oto3.html", "oto4.html", "oto5.html"]

print("%-10s %-14s %-8s %s" % ("page", "no-thanks ->", "exists", "checkout"))
ok = True
for f in chain:
    h = open(f, encoding="utf-8").read()
    m = re.search(r'no:\s*"([^"]*)"', h)
    target = m.group(1) if m else "??"
    exists = os.path.exists(target)
    buy = re.search(r'buy:\s*"([^"]*)"', h)
    buy_url = buy.group(1) if buy else ""
    ok = ok and exists
    print("%-10s %-14s %-8s %s" % (
        f, target, "yes" if exists else "NO",
        buy_url or "(empty - paste the checkout URL)"))

stray = [p for p in os.listdir(".") if re.fullmatch(r"ds\d+\.html", p)]
if stray:
    print("\nWARNING: downsell files still present:", ", ".join(sorted(stray)))
    ok = False

print()
print("chain intact, no downsells" if ok else "PROBLEMS FOUND")
