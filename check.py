#!/usr/bin/env python3
"""Pre-deploy checks for mohammadkhalikujjaman.com.

Run from the site root:  python3 check.py     (macOS/Linux)
                         python  check.py     (Windows - python3 is not on PATH here)

Exits non-zero if anything fails, so it can gate a deploy.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
CANONICAL = "https://mohammadkhalikujjaman.com/"

failures = []


def fail(msg):
    failures.append(msg)


def check_asset_references(html):
    """Every /docs/, /projects/ and /profile/ reference must resolve on disk."""
    refs = re.findall(r'(?:href|src)="(/(?:docs|projects|profile)/[^"]+)"', html)
    if not refs:
        fail("no /docs, /projects or /profile references found at all - check the paths")
    for ref in sorted(set(refs)):
        if not (ROOT / ref.lstrip("/")).is_file():
            fail("missing file: %s" % ref)

    # the reverse direction: files on disk nothing links to
    for folder in ("docs", "projects", "profile"):
        for path in sorted((ROOT / folder).glob("*")):
            if path.name.startswith("."):
                continue
            if "/%s/%s" % (folder, path.name) not in html:
                fail("orphan file, nothing links to it: /%s/%s" % (folder, path.name))


def check_images(html):
    """No <img> may lack alt text or explicit dimensions."""
    for tag in re.findall(r"<img\b[^>]*>", html):
        src = re.search(r'src="([^"]*)"', tag)
        name = src.group(1) if src else tag[:60]
        if not re.search(r'\balt="[^"]+"', tag):
            fail("img has empty or missing alt: %s" % name)
        for dim in ("width", "height"):
            if not re.search(r'\b%s="\d+"' % dim, tag):
                fail("img has no explicit %s: %s" % (dim, name))
        if 'loading="lazy"' not in tag and "hero" not in name:
            fail("img is not lazy-loaded: %s" % name)


def check_jsonld(html):
    """The JSON-LD Person block must parse and keep its sameAs array."""
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    if len(blocks) != 1:
        fail("expected exactly 1 JSON-LD block, found %d" % len(blocks))
        return
    try:
        data = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        fail("JSON-LD does not parse: %s" % exc)
        return
    if data.get("@type") != "Person":
        fail("JSON-LD @type is not Person")
    if not data.get("sameAs"):
        fail("JSON-LD sameAs array is missing or empty")
    else:
        for required in ("linkedin.com", "orcid.org"):
            if not any(required in s for s in data["sameAs"]):
                fail("JSON-LD sameAs no longer lists %s" % required)


def check_head(html):
    """Canonical URL and the indexing directives must survive every edit."""
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    if not canonical:
        fail("canonical link is missing")
    elif canonical.group(1) != CANONICAL:
        fail("canonical URL changed: %s" % canonical.group(1))

    if '<meta name="robots" content="index, follow">' not in html:
        fail("robots meta is missing or no longer 'index, follow'")
    if "<title>Mohammad Khalikujjaman | Mechanical Engineer</title>" not in html:
        fail("title changed")
    for prop in ("og:title", "og:image", "twitter:card", "description", "keywords"):
        if prop not in html:
            fail("head is missing %s" % prop)


def check_anchors(html):
    """Every in-page anchor must have a matching id."""
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    for anchor in sorted(set(re.findall(r'href="#([^"]+)"', html))):
        if anchor not in ids:
            fail("anchor #%s has no matching element" % anchor)


def check_no_react_remnants(html):
    """Nothing from the old server-rendered build may survive."""
    for needle, label in (
        ("VINEXT", "React RSC payload"),
        ("modulepreload", "modulepreload link"),
        ("Mechanical Engineer_files", "Chrome save-page path"),
        ("__CF$cv$params", "Cloudflare challenge script"),
        ("data-qb-installed", "browser-extension attribute"),
        ("_source/", "reference into the _source stash"),
    ):
        if needle in html:
            fail("%s still present in index.html" % label)


def check_sitemap():
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        fail("sitemap.xml is missing")
        return
    text = sitemap.read_text(encoding="utf-8")
    if CANONICAL not in text:
        fail("sitemap.xml does not list the canonical URL")
    if not re.search(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", text):
        fail("sitemap.xml has no valid <lastmod>")
    robots = ROOT / "robots.txt"
    if not robots.is_file():
        fail("robots.txt is missing")
    elif "Sitemap: %ssitemap.xml" % CANONICAL not in robots.read_text(encoding="utf-8"):
        fail("robots.txt does not point at the sitemap")
    for name in ("favicon.svg", "favicon.ico", "social-card.png", "assets/site.css"):
        if not (ROOT / name).is_file():
            fail("missing root asset: %s" % name)


def check_github_pages():
    """Deploy-target requirements for GitHub Pages."""
    if not (ROOT / ".nojekyll").is_file():
        fail(".nojekyll is missing - GitHub Pages will run Jekyll over the site")

    for stale in ("_headers", "_redirects"):
        if (ROOT / stale).is_file():
            fail("%s is present but GitHub Pages ignores it - it does nothing here" % stale)

    # GitHub writes this file when you set the custom domain in the repo settings.
    cname = ROOT / "CNAME"
    if cname.is_file():
        got = cname.read_text(encoding="utf-8").strip()
        want = CANONICAL.split("//")[1].rstrip("/")
        if got != want:
            fail("CNAME says %r, expected %r - the custom domain will not match" % (got, want))


def main():
    if not INDEX.is_file():
        print("FAIL  index.html not found - run this from the site root")
        return 1
    html = INDEX.read_text(encoding="utf-8")

    check_asset_references(html)
    check_images(html)
    check_jsonld(html)
    check_head(html)
    check_anchors(html)
    check_no_react_remnants(html)
    check_sitemap()
    check_github_pages()

    if failures:
        print("FAIL  %d problem(s):\n" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1
    print("PASS  index.html, %d docs, %d project images, sitemap and robots all check out"
          % (len(list((ROOT / "docs").glob("*.pdf"))),
             len(list((ROOT / "projects").glob("*")))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
