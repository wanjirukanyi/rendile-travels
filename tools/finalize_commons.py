#!/usr/bin/env python3
"""Download chosen Commons originals via the 1280px thumbnailer.
Usage: finalize_commons.py <dest_dir> <slug>::<FULL upload.wikimedia.org url> ...
"""
import sys, os, urllib.request

UA = "RendileTravels/1.0 (maureenkanyi@gmail.com) educational-site"

def thumb_url(full, width=1280):
    marker = "/commons/"; i = full.index(marker) + len(marker)
    prefix, rest = full[:i], full[i:]
    parts = rest.split("/"); name = parts[-1]; hashdir = "/".join(parts[:-1])
    return f"{prefix}thumb/{hashdir}/{name}/{width}px-{name}"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read()

dest = sys.argv[1]; os.makedirs(dest, exist_ok=True)
for arg in sys.argv[2:]:
    slug, full = arg.split("::", 1)
    out = os.path.join(dest, slug + ".jpg")
    try: data = get(thumb_url(full))
    except Exception as e:
        print(f"{slug}: thumb failed ({e}); trying original"); data = get(full)
    with open(out,"wb") as f: f.write(data)
    print(f"{slug}: {len(data)//1024} KB -> {out}")
