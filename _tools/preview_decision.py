#!/usr/bin/env python3
"""Extract the last section (decision block) of a generated page into a
standalone HTML file so it can be screenshotted on its own."""
import re
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

src = sys.argv[1] if len(sys.argv) > 1 else "oto1.html"
out = sys.argv[2] if len(sys.argv) > 2 else "_shots/decision.html"

html = open(src, encoding="utf-8").read()
m = re.search(r'<section class="bs-decision".*?</section>', html, re.S)
if not m:
    raise SystemExit("decision section not found in " + src)

# The preview lives in _shots/, one level below the stylesheet.
prefix = "../" if os.path.dirname(out) else ""

page = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>decision preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter+Tight:ital,wght@0,400;0,500;0,600;0,700;0,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%scss/oto.css">
</head>
<body class="bs-oto">
%s
</body></html>""" % (prefix, m.group(0))

open(out, "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out, "from", src)
