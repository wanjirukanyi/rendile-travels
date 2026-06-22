#!/usr/bin/env python3
"""Stage Wikimedia Commons image candidates for visual verification.
Usage: fetch_commons.py <stage_dir> <slug>::<search query> [<slug>::<query> ...]
"""
import sys, json, os, urllib.parse, urllib.request, re

UA = "RendileTravels/1.0 (maureenkanyi@gmail.com) educational-site"
API = "https://commons.wikimedia.org/w/api.php"
N = 4
THUMB = 500
OK_LIC = ("cc-by", "cc0", "cc-zero", "public", "pd-")
BAD = ("-nc", "noncommercial", "non-commercial", "fair use", "non-free")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read()

def meta_val(em, key):
    try: return em[key]["value"]
    except Exception: return ""

def search(query):
    params = {"action":"query","format":"json","prop":"imageinfo","generator":"search",
        "gsrsearch":query,"gsrnamespace":"6","gsrlimit":str(N+4),
        "iiprop":"url|extmetadata|size|mime","iiurlwidth":str(THUMB)}
    data = json.loads(get(API + "?" + urllib.parse.urlencode(params)))
    pages = data.get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 999))

def main():
    stage = sys.argv[1]; os.makedirs(stage, exist_ok=True)
    for arg in sys.argv[2:]:
        slug, query = arg.split("::", 1)
        print(f"\n===== {slug}  <<{query}>>")
        n = 0
        for p in search(query):
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("mime","") not in ("image/jpeg","image/png"): continue
            em = ii.get("extmetadata", {})
            blob = (meta_val(em,"LicenseShortName").lower()+" "+meta_val(em,"License").lower())
            if any(b in blob for b in BAD): continue
            if not any(o in blob for o in OK_LIC): continue
            thumb = ii.get("thumburl")
            if not thumb: continue
            n += 1
            dest = os.path.join(stage, f"{slug}-{n}.jpg")
            try:
                with open(dest,"wb") as f: f.write(get(thumb))
            except Exception as e:
                print(f"  [{n}] DL FAIL {e}"); continue
            author = re.sub("<[^>]+>","",meta_val(em,"Artist")).strip()[:60]
            print(f"  [{n}] {ii.get('width')}x{ii.get('height')} {meta_val(em,'LicenseShortName')} | {author}")
            print(f"       {p.get('title','').replace('File:','')}")
            print(f"       FULL {ii.get('url')}")
            if n >= N: break
        if n == 0: print("  (no suitable candidates)")

if __name__ == "__main__": main()
