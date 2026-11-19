#!/usr/bin/env python3
"""Swap the JV launch-doc and promo-swipes links in both JV pages.

Byte-safe: reads and writes UTF-8 without touching anything else, so the
page's non-ASCII characters (middot, arrows, symbols) survive untouched.
"""
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OLD_DOC = ("https://docs.google.com/document/d/1XjpZt8-vXPwjCnx27KPXZibirjuilrOw"
           "/edit?usp=sharing&amp;ouid=109116930590810602541&amp;rtpof=true&amp;sd=true")
NEW_DOC = "https://docs.google.com/document/d/1hJCF1QbmFu-k0kQDxEZOHvdoSHrTunAj/edit"

OLD_SWIPE = ("https://docs.google.com/document/d/1CINgtCMWZ4T9EDAMsbYtvAjLYdgUeCfOxdk41im6tiM"
             "/edit?usp=sharing")
NEW_SWIPE = ("https://docs.google.com/document/d/1BfEoHrV5HX176rhOHbfAFQx28yab9i1nURKCPtey6nE"
             "/edit?tab=t.0#heading=h.u5lv8n9gub7r")

TARGETS = ["jv.html", os.path.join("jv", "index.html")]

failed = False
for path in TARGETS:
    with open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()

    docs = text.count(OLD_DOC)
    swipes = text.count(OLD_SWIPE)

    text = text.replace(OLD_DOC, NEW_DOC).replace(OLD_SWIPE, NEW_SWIPE)

    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    left_doc = text.count(OLD_DOC)
    left_swipe = text.count(OLD_SWIPE)
    new_doc = text.count(NEW_DOC)
    new_swipe = text.count(NEW_SWIPE)

    print("%-16s replaced doc=%d swipe=%d | now new_doc=%d new_swipe=%d | old left=%d/%d"
          % (path, docs, swipes, new_doc, new_swipe, left_doc, left_swipe))

    if docs == 0 or swipes == 0 or left_doc or left_swipe:
        failed = True

sys.exit(1 if failed else 0)
