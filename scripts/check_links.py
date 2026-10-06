#!/usr/bin/env python3
"""Fail if index.html references a local file that does not exist,
uses a dead href="#", or still contains template placeholder text."""
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
PLACEHOLDERS = ["lorem ipsum", "richard hanrick", "jessica miller", "emily evans", "daniel lewis", "example.com"]


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("src", "href") and value is not None:
                self.refs.append((tag, name, value))


def main() -> int:
    html = PAGE.read_text(encoding="utf-8")
    parser = Refs()
    parser.feed(html)
    errors = []
    for tag, attr, value in parser.refs:
        if value in ("#", ""):
            errors.append(f"dead link: <{tag} {attr}=\"{value}\">")
            continue
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", value) or value.startswith("//"):
            continue
        target = (ROOT / value.split("#")[0].split("?")[0]).resolve()
        if not target.exists():
            errors.append(f"missing file: {value}")
    css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
    for url in re.findall(r"url\(['\"]?([^'\")]+)", css):
        if not re.match(r"^(https?:|data:)", url) and not (ROOT / "assets/css" / url).resolve().exists():
            errors.append(f"missing CSS asset: {url}")
    lowered = html.lower()
    for word in PLACEHOLDERS:
        if word in lowered:
            errors.append(f"placeholder text found: {word}")
    if "tel:" in lowered:
        errors.append("phone number link found (keep personal phone off the public page)")
    for e in errors:
        print(e)
    print(f"checked {len(parser.refs)} references: {'FAIL' if errors else 'OK'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
