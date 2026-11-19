#!/usr/bin/env python3
"""Extract one <section> (by id) from a generated page into a standalone
preview file so it can be screenshotted reliably at a normal viewport."""
import os
import re
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

src = sys.argv[1]
section_id = sys.argv[2]
out = sys.argv[3]

html = open(src, encoding="utf-8").read()

# grab the section whose tag contains id="<section_id>"
pattern = re.compile(r'<section[^>]*id="%s"[^>]*>.*?</section>' % re.escape(section_id), re.S)
m = pattern.search(html)
if not m:
    raise SystemExit("section #%s not found in %s" % (section_id, src))

prefix = "../" if os.path.dirname(out) else ""

body = m.group(0)
if prefix:
    # The preview lives one level down, so relative asset paths need ../.
    body = re.sub(r'(src|href)="(images|css|js|f)/', r'\1="%s\2/' % prefix, body)
    body = re.sub(r"url\('(images|css|js|f)/", r"url('%s\1/" % prefix, body)

page = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>preview %s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter+Tight:ital,wght@0,400;0,500;0,600;0,700;0,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%scss/oto.css">
</head>
<body class="bs-oto">
%s
</body></html>""" % (section_id, prefix, body)

open(out, "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out)
